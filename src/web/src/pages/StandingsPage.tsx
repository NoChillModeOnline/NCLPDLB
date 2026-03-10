import { useQuery } from "@tanstack/react-query";
import { api, Standing } from "../api/client";

const GUILD_ID = import.meta.env.VITE_GUILD_ID ?? "default";

function EloBar({ elo }: { elo: number }) {
  const pct = Math.min(100, Math.max(0, ((elo - 800) / 800) * 100));
  return (
    <div className="w-24 h-2 bg-slate-700 rounded-full overflow-hidden">
      <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${pct}%` }} />
    </div>
  );
}

function StreakBadge({ streak }: { streak: number }) {
  if (streak === 0) return null;
  const positive = streak > 0;
  return (
    <span
      className={`text-xs px-2 py-0.5 rounded-full font-medium ${
        positive ? "bg-green-900 text-green-300" : "bg-red-900 text-red-300"
      }`}
    >
      {positive ? `+${streak}🔥` : `${streak}❄️`}
    </span>
  );
}

export default function StandingsPage() {
  const { data: standings, isLoading } = useQuery({
    queryKey: ["standings", GUILD_ID],
    queryFn: () => api.leagues.standings(GUILD_ID),
    refetchInterval: 60_000,
  });

  if (isLoading) return <div className="text-slate-400 animate-pulse">Loading standings…</div>;
  if (!standings?.length) return <div className="text-slate-500">No standings data yet.</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Standings</h1>
      <div className="overflow-x-auto rounded-xl border border-slate-700">
        <table className="w-full text-sm">
          <thead className="bg-slate-800 text-slate-400 text-xs uppercase tracking-wide">
            <tr>
              {["#", "Player", "ELO", "W", "L", "Win %", "Streak"].map((h) => (
                <th key={h} className="px-4 py-3 text-left font-medium">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {standings.map((s: Standing, i: number) => (
              <tr key={s.player_id} className="hover:bg-slate-800/50 transition-colors">
                <td className="px-4 py-3 font-bold text-slate-400">{i + 1}</td>
                <td className="px-4 py-3 font-medium">{s.display_name || s.player_id.slice(0, 8)}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-indigo-300">{s.elo}</span>
                    <EloBar elo={s.elo} />
                  </div>
                </td>
                <td className="px-4 py-3 text-green-400 font-medium">{s.wins}</td>
                <td className="px-4 py-3 text-red-400 font-medium">{s.losses}</td>
                <td className="px-4 py-3 text-slate-300">{s.win_rate.toFixed(1)}%</td>
                <td className="px-4 py-3">
                  <StreakBadge streak={s.streak} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
