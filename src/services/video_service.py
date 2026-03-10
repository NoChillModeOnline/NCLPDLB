"""
Video Upload Service — Cross-platform upload to Cloudflare R2 (free) or Azure Blob (Path B).
Supports MP4, MOV, AVI from capture cards. Optional ffmpeg thumbnail generation.
"""
from __future__ import annotations

import logging
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import discord

from src.config import settings
from src.data.sheets import sheets

log = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {"video/mp4", "video/quicktime", "video/x-msvideo", "video/avi"}
MAX_FILE_SIZE_MB = 100


@dataclass
class VideoUploadResult:
    success: bool
    video_id: str = ""
    public_url: str = ""
    thumbnail_url: str = ""
    error: str = ""


class VideoService:
    async def upload_match_video(
        self,
        guild_id: str,
        uploader_id: str,
        opponent_id: str,
        attachment: discord.Attachment,
        notes: str = "",
    ) -> VideoUploadResult:
        if attachment.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            return VideoUploadResult(
                success=False,
                error=f"File too large. Max {MAX_FILE_SIZE_MB}MB. Consider uploading to YouTube and sharing the link instead."
            )

        video_id = str(uuid.uuid4())[:12]
        file_ext = Path(attachment.filename).suffix.lower() or ".mp4"
        object_key = f"matches/{guild_id}/{video_id}{file_ext}"

        # Download attachment bytes
        try:
            video_bytes = await attachment.read()
        except Exception as e:
            return VideoUploadResult(success=False, error=f"Failed to read attachment: {e}")

        # Upload based on deployment target
        if settings.video_storage_backend == "azure":
            result = await self._upload_azure(object_key, video_bytes, attachment.content_type or "video/mp4")
        else:
            result = await self._upload_r2(object_key, video_bytes, attachment.content_type or "video/mp4")

        if not result.success:
            return result

        # Optional thumbnail via ffmpeg
        thumbnail_url = ""
        if shutil.which(settings.ffmpeg_path):
            thumbnail_url = await self._generate_thumbnail(video_id, video_bytes, file_ext)

        # Save metadata to Google Sheets
        sheets.save_video({
            "video_id": video_id,
            "match_id": "",
            "uploader_id": uploader_id,
            "opponent_id": opponent_id,
            "storage_url": result.public_url,
            "thumbnail_url": thumbnail_url,
            "notes": notes,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        log.info(f"Video {video_id} uploaded by {uploader_id} in guild {guild_id}")
        return VideoUploadResult(
            success=True,
            video_id=video_id,
            public_url=result.public_url,
            thumbnail_url=thumbnail_url,
        )

    async def _upload_r2(self, key: str, data: bytes, content_type: str) -> VideoUploadResult:
        """Upload to Cloudflare R2 via S3-compatible API (free 10GB/mo, $0 egress)."""
        try:
            import boto3

            endpoint = f"https://{settings.r2_account_id}.r2.cloudflarestorage.com"
            s3 = boto3.client(
                "s3",
                endpoint_url=endpoint,
                aws_access_key_id=settings.r2_access_key_id,
                aws_secret_access_key=settings.r2_secret_access_key,
                region_name="auto",
            )
            s3.put_object(
                Bucket=settings.r2_bucket_name,
                Key=key,
                Body=data,
                ContentType=content_type,
            )
            public_url = f"{settings.r2_public_url}/{key}" if settings.r2_public_url else ""
            return VideoUploadResult(success=True, public_url=public_url)
        except Exception as e:
            log.error(f"R2 upload error: {e}", exc_info=True)
            return VideoUploadResult(success=False, error=f"R2 upload failed: {e}")

    async def _upload_azure(self, key: str, data: bytes, content_type: str) -> VideoUploadResult:
        """Upload to Azure Blob Storage (Path B deployment)."""
        try:
            from azure.storage.blob import BlobServiceClient

            client = BlobServiceClient.from_connection_string(settings.azure_storage_connection_string)
            container = client.get_container_client(settings.azure_storage_container)
            blob = container.get_blob_client(key)
            blob.upload_blob(data, overwrite=True, content_settings={"content_type": content_type})
            public_url = blob.url
            return VideoUploadResult(success=True, public_url=public_url)
        except Exception as e:
            log.error(f"Azure upload error: {e}", exc_info=True)
            return VideoUploadResult(success=False, error=f"Azure upload failed: {e}")

    async def _generate_thumbnail(self, video_id: str, video_bytes: bytes, ext: str) -> str:
        """
        Generate thumbnail using ffmpeg (cross-platform — uses PATH or configured ffmpeg_path).
        Windows: winget install Gyan.FFmpeg
        macOS:   brew install ffmpeg
        Linux:   apt install ffmpeg
        """
        try:
            import asyncio
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                video_file = tmp_path / f"input{ext}"
                thumb_file = tmp_path / "thumb.jpg"
                video_file.write_bytes(video_bytes)

                proc = await asyncio.create_subprocess_exec(
                    settings.ffmpeg_path,
                    "-i", str(video_file),
                    "-ss", "00:00:03",
                    "-vframes", "1",
                    "-q:v", "2",
                    str(thumb_file),
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                await asyncio.wait_for(proc.wait(), timeout=30)

                if thumb_file.exists():
                    thumb_bytes = thumb_file.read_bytes()
                    thumb_key = f"thumbnails/{video_id}.jpg"
                    if settings.video_storage_backend == "azure":
                        r = await self._upload_azure(thumb_key, thumb_bytes, "image/jpeg")
                    else:
                        r = await self._upload_r2(thumb_key, thumb_bytes, "image/jpeg")
                    return r.public_url
        except Exception as e:
            log.warning(f"Thumbnail generation failed (non-fatal): {e}")
        return ""
