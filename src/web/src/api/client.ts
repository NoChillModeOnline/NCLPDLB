const BASE = "/api";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`);
  return res.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`);
  return res.json();
}

export const api = {
  pokemon: {
    list: (params?: { tier?: string; gen?: number; search?: string }) => {
      const q = new URLSearchParams();
      if (params?.tier) q.set("tier", params.tier);
      if (params?.gen) q.set("gen", String(params.gen));
      if (params?.search) q.set("search", params.search);
      return get<Pokemon[]>(`/pokemon?${q}`);
    },
    get: (name: string) => get<Pokemon>(`/pokemon/${encodeURIComponent(name)}`),
  },
  drafts: {
    list: (guildId: string) => get<Draft>(`/drafts/${guildId}`),
    pick: (guildId: string, playerId: string, pokemonName: string) =>
      post<PickResult>(`/drafts/${guildId}/pick`, { player_id: playerId, pokemon_name: pokemonName }),
  },
  teams: {
    get: (guildId: string, playerId: string) => get<Team>(`/teams/${guildId}/${playerId}`),
    analysis: (guildId: string, playerId: string) =>
      get<TeamAnalysis>(`/teams/${guildId}/${playerId}/analysis`),
  },
  leagues: {
    standings: (guildId: string) => get<Standing[]>(`/leagues/${guildId}/standings`),
  },
  matchups: {
    compare: (guildId: string, p1: string, p2: string) =>
      get<MatchupResult>(`/matchups/${guildId}/${p1}/${p2}`),
  },
};

// ── WebSocket ─────────────────────────────────────────────────

export function createDraftSocket(
  guildId: string,
  onMessage: (event: DraftEvent) => void
): WebSocket {
  const proto = location.protocol === "https:" ? "wss:" : "ws:";
  const ws = new WebSocket(`${proto}//${location.host}/ws/${guildId}`);
  ws.onmessage = (e) => {
    try {
      onMessage(JSON.parse(e.data));
    } catch {
      // ignore malformed messages
    }
  };
  return ws;
}

// ── Types ─────────────────────────────────────────────────────

export interface Pokemon {
  national_dex: number;
  name: string;
  types: string[];
  base_stats: { hp: number; atk: number; def: number; spa: number; spd: number; spe: number };
  abilities: string[];
  hidden_ability: string | null;
  generation: number;
  is_legendary: boolean;
  is_mythical: boolean;
  showdown_tier: string;
  vgc_legal: boolean;
  tier_points: number;
  sprite_url: string;
  sprite_url_shiny: string;
  sprite_url_back: string;
}

export interface DraftPick {
  pick_id: string;
  draft_id: string;
  player_id: string;
  pokemon_name: string;
  round: number;
  pick_number: number;
}

export interface Draft {
  draft_id: string;
  guild_id: string;
  format: "snake" | "auction" | "tiered" | "custom";
  status: "setup" | "ban_phase" | "active" | "paused" | "completed";
  total_rounds: number;
  current_round: number;
  player_order: string[];
  current_player_id: string | null;
  picks: DraftPick[];
}

export interface Team {
  team_id: string;
  player_id: string;
  pokemon: Pokemon[];
}

export interface TeamAnalysis {
  coverage_summary: string;
  weakness_summary: string;
  speed_summary: string;
  archetype: string;
  threat_score: number;
}

export interface Standing {
  player_id: string;
  display_name: string;
  elo: number;
  wins: number;
  losses: number;
  win_rate: number;
  streak: number;
}

export interface PickResult {
  success: boolean;
  error?: string;
  pokemon?: Pokemon;
  next_player_name?: string;
}

export interface MatchupResult {
  player1_id: string;
  player2_id: string;
  advantage_score: number;
  summary: string;
  details: string[];
}

export interface DraftEvent {
  type: "pick" | "ban" | "start" | "complete" | "skip";
  payload: Record<string, unknown>;
}
