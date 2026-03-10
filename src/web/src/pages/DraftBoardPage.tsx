import { useEffect, useRef, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { api, createDraftSocket, DraftEvent, DraftPick } from "../api/client";

const GUILD_ID = import.meta.env.VITE_GUILD_ID ?? "default";

function PokemonCard({ name, round, pick }: { name: string; round: number; pick: number }) {
  const { data: poke } = useQuery({
    queryKey: ["pokemon", name],
    queryFn: () => api.pokemon.get(name),
    staleTime: Infinity,
  });
  return (
    <div className="flex items-center gap-2 bg-slate-800 rounded-lg px-3 py-2 text-sm">
      {poke && (
        <img src={poke.sprite_url} alt={poke.name} className="w-10 h-10 object-contain" />
      )}
      <div>
        <div className="font-medium">{name}</div>
        <div className="text-xs text-slate-400">R{round} · #{pick}</div>
      </div>
    </div>
  );
}

function PlayerColumn({
  playerId,
  picks,
  isCurrent,
}: {
  playerId: string;
  picks: DraftPick[];
  isCurrent: boolean;
}) {
  const myPicks = picks.filter((p) => p.player_id === playerId);
  return (
    <div
      className={`flex-1 min-w-0 rounded-xl border p-3 ${
        isCurrent ? "border-indigo-500 bg-indigo-950/40" : "border-slate-700 bg-slate-900"
      }`}
    >
      <div className={`text-xs font-semibold mb-2 truncate ${isCurrent ? "text-indigo-300" : "text-slate-400"}`}>
        {isCurrent && <span className="mr-1">▶</span>}
        {playerId.slice(0, 8)}…
      </div>
      <div className="flex flex-col gap-1">
        {myPicks.map((p) => (
          <PokemonCard key={p.pick_id} name={p.pokemon_name} round={p.round} pick={p.pick_number} />
        ))}
        {myPicks.length === 0 && (
          <div className="text-xs text-slate-600 italic">No picks yet</div>
        )}
      </div>
    </div>
  );
}

export default function DraftBoardPage() {
  const queryClient = useQueryClient();
  const wsRef = useRef<WebSocket | null>(null);
  const [liveStatus, setLiveStatus] = useState<string>("");

  const { data: draft, isLoading } = useQuery({
    queryKey: ["draft", GUILD_ID],
    queryFn: () => api.drafts.list(GUILD_ID),
    refetchInterval: 30_000,
  });

  useEffect(() => {
    const ws = createDraftSocket(GUILD_ID, (event: DraftEvent) => {
      if (event.type === "pick" || event.type === "ban" || event.type === "skip") {
        queryClient.invalidateQueries({ queryKey: ["draft", GUILD_ID] });
        setLiveStatus(`Last event: ${event.type}`);
      }
    });
    wsRef.current = ws;
    return () => ws.close();
  }, [queryClient]);

  if (isLoading) return <div className="text-slate-400 animate-pulse">Loading draft…</div>;
  if (!draft) return <div className="text-slate-500">No active draft found for this server.</div>;

  const statusColor: Record<string, string> = {
    active: "text-green-400",
    paused: "text-yellow-400",
    completed: "text-slate-400",
    setup: "text-blue-400",
    ban_phase: "text-red-400",
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Live Draft Board</h1>
          <p className="text-sm text-slate-400 mt-1">
            Round {draft.current_round} / {draft.total_rounds} ·{" "}
            <span className={statusColor[draft.status] ?? "text-slate-300"}>
              {draft.status.replace("_", " ").toUpperCase()}
            </span>
          </p>
        </div>
        {liveStatus && (
          <span className="text-xs bg-indigo-900 text-indigo-200 px-3 py-1 rounded-full">
            🔴 Live · {liveStatus}
          </span>
        )}
      </div>

      <div className="flex gap-3 overflow-x-auto pb-2">
        {draft.player_order.map((pid) => (
          <PlayerColumn
            key={pid}
            playerId={pid}
            picks={draft.picks}
            isCurrent={pid === draft.current_player_id}
          />
        ))}
      </div>

      <div className="text-xs text-slate-600 text-center">
        Draft ID: {draft.draft_id} · {draft.picks.length} picks recorded
      </div>
    </div>
  );
}
