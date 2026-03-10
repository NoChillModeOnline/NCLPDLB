import { useQuery } from "@tanstack/react-query";
import { api, Standing } from "../api/client";

const GUILD_ID = import.meta.env.VITE_GUILD_ID ?? "default";

interface Matchup {
  p1: Standing;
  p2: Standing;
  eloDiff: number;
}

function buildRoundRobin(standings: Standing[]): Matchup[] {
  const matchups: Matchup[] = [];
  for (let i = 0; i < standings.length; i++) {
    for (let j = i + 1; j < standings.length; j++) {
      matchups.push({
        p1: standings[i],
        p2: standings[j],
        eloDiff: Math.abs(standings[i].elo - standings[j].elo),
      });
    }
  }
  return matchups.sort((a, b) => a.eloDiff - b.eloDiff);
}

function MatchCard({ matchup }: { matchup: Matchup }) {
  const { p1, p2, eloDiff } = matchup;
  const favorite = p1.elo >= p2.elo ? p1 : p2;
  const underdog = p1.elo >= p2.elo ? p2 : p1;

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
      <div className="flex items-center justify-between gap-4">
        <div className="flex-1 text-right">
          <div className="font-semibold">{favorite.display_name || favorite.player_id.slice(0, 8)}</div>
          <div className="text-sm text-indigo-300 font-mono">{favorite.elo} ELO</div>
          <div className="text-xs text-slate-400">{favorite.wins}W – {favorite.losses}L</div>
        </div>
        <div className="text-slate-500 font-bold text-lg shrink-0">VS</div>
        <div className="flex-1">
          <div className="font-semibold">{underdog.display_name || underdog.player_id.slice(0, 8)}</div>
          <div className="text-sm text-indigo-300 font-mono">{underdog.elo} ELO</div>
          <div className="text-xs text-slate-400">{underdog.wins}W – {underdog.losses}L</div>
        </div>
      </div>
      <div className="mt-3 text-xs text-center text-slate-500">
        ELO gap: {eloDiff} pts
      </div>
    </div>
  );
}

export default function SchedulePage() {
  const { data: standings, isLoading } = useQuery({
    queryKey: ["standings", GUILD_ID],
    queryFn: () => api.leagues.standings(GUILD_ID),
  });

  if (isLoading) return <div className="text-slate-400 animate-pulse">Loading schedule…</div>;
  if (!standings?.length) return <div className="text-slate-500">No players in the league yet.</div>;

  const matchups = buildRoundRobin(standings);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Schedule</h1>
        <p className="text-sm text-slate-400 mt-1">
          Suggested matchups sorted by closest ELO — {matchups.length} total
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {matchups.map((m) => (
          <MatchCard key={`${m.p1.player_id}-${m.p2.player_id}`} matchup={m} />
        ))}
      </div>
    </div>
  );
}
