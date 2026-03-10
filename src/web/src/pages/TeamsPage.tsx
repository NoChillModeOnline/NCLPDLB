import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, Pokemon } from "../api/client";

const GUILD_ID = import.meta.env.VITE_GUILD_ID ?? "default";

const TYPE_COLORS: Record<string, string> = {
  fire: "bg-orange-700", water: "bg-blue-700", grass: "bg-green-700",
  electric: "bg-yellow-600", psychic: "bg-pink-700", ice: "bg-cyan-700",
  dragon: "bg-purple-800", dark: "bg-gray-700", fairy: "bg-pink-600",
  normal: "bg-gray-600", fighting: "bg-red-800", poison: "bg-purple-700",
  ground: "bg-yellow-700", flying: "bg-indigo-600", bug: "bg-lime-700",
  rock: "bg-stone-600", ghost: "bg-violet-800", steel: "bg-slate-600",
};

function TypeBadge({ type }: { type: string }) {
  const color = TYPE_COLORS[type] ?? "bg-slate-600";
  return (
    <span className={`text-xs px-2 py-0.5 rounded font-medium text-white ${color}`}>
      {type}
    </span>
  );
}

function PokemonRow({ poke }: { poke: Pokemon }) {
  const [showShiny, setShowShiny] = useState(false);
  return (
    <div className="flex items-center gap-4 bg-slate-800 rounded-lg p-3 hover:bg-slate-750 transition-colors">
      <button
        className="shrink-0 w-14 h-14 cursor-pointer"
        onClick={() => setShowShiny((s) => !s)}
        title="Click to toggle shiny"
      >
        <img
          src={showShiny ? poke.sprite_url_shiny : poke.sprite_url}
          alt={poke.name}
          className="w-full h-full object-contain"
        />
      </button>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="font-semibold">{poke.name}</span>
          {poke.types.map((t) => <TypeBadge key={t} type={t} />)}
          <span className="text-xs text-slate-400 ml-auto">{poke.showdown_tier}</span>
        </div>
        <div className="text-xs text-slate-400 mt-1 font-mono">
          HP {poke.base_stats.hp} · Atk {poke.base_stats.atk} · Def {poke.base_stats.def} ·
          SpA {poke.base_stats.spa} · SpD {poke.base_stats.spd} · Spe {poke.base_stats.spe}
        </div>
      </div>
    </div>
  );
}

function TeamView({ playerId }: { playerId: string }) {
  const { data: team, isLoading } = useQuery({
    queryKey: ["team", GUILD_ID, playerId],
    queryFn: () => api.teams.get(GUILD_ID, playerId),
    enabled: !!playerId,
  });
  const { data: analysis } = useQuery({
    queryKey: ["analysis", GUILD_ID, playerId],
    queryFn: () => api.teams.analysis(GUILD_ID, playerId),
    enabled: !!playerId,
  });

  if (isLoading) return <div className="text-slate-400 animate-pulse">Loading team…</div>;
  if (!team) return <div className="text-slate-500">No team found.</div>;

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2">
        {team.pokemon.map((p) => <PokemonRow key={p.national_dex} poke={p} />)}
      </div>
      {analysis && (
        <div className="grid grid-cols-2 gap-3 mt-4">
          {[
            ["Coverage", analysis.coverage_summary],
            ["Weaknesses", analysis.weakness_summary],
            ["Speed Tiers", analysis.speed_summary],
            ["Archetype", analysis.archetype],
          ].map(([label, value]) => (
            <div key={label} className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 font-medium mb-1">{label}</div>
              <div className="text-sm">{value}</div>
            </div>
          ))}
          <div className="bg-slate-800 rounded-lg p-3 col-span-2">
            <div className="text-xs text-slate-400 font-medium mb-1">Threat Score</div>
            <div className="text-2xl font-bold text-indigo-300">{analysis.threat_score}</div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function TeamsPage() {
  const [playerId, setPlayerId] = useState("");
  const [submitted, setSubmitted] = useState("");

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Teams</h1>
      <div className="flex gap-3">
        <input
          className="flex-1 bg-slate-800 border border-slate-600 rounded-lg px-4 py-2 text-sm outline-none focus:border-indigo-500"
          placeholder="Enter Discord User ID..."
          value={playerId}
          onChange={(e) => setPlayerId(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && setSubmitted(playerId)}
        />
        <button
          className="bg-indigo-600 hover:bg-indigo-500 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          onClick={() => setSubmitted(playerId)}
        >
          View Team
        </button>
      </div>
      {submitted && <TeamView playerId={submitted} />}
    </div>
  );
}
