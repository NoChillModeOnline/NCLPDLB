import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, Pokemon } from "../api/client";

const TIERS = ["", "Uber", "OU", "UUBL", "UU", "RUBL", "RU", "NUBL", "NU", "PUBL", "PU", "NFE", "LC", "AG", "Untiered"];
const GENS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

const TYPE_COLORS: Record<string, string> = {
  fire: "#C13A2F", water: "#2775C7", grass: "#4A9230",
  electric: "#D4B816", psychic: "#C24884", ice: "#4FC5C5",
  dragon: "#4B3D9C", dark: "#4A4056", fairy: "#C67AC8",
  normal: "#8B8B8B", fighting: "#923428", poison: "#7B3A92",
  ground: "#B08B2F", flying: "#5B70B8", bug: "#6A8C16",
  rock: "#8B7040", ghost: "#5C4985", steel: "#607090",
};

function StatBar({ value, max = 255 }: { value: number; max?: number }) {
  const pct = (value / max) * 100;
  const color = pct > 66 ? "#4ade80" : pct > 33 ? "#facc15" : "#f87171";
  return (
    <div className="flex items-center gap-2">
      <div className="w-24 h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span className="text-xs font-mono w-8 text-right">{value}</span>
    </div>
  );
}

function PokemonCard({ poke }: { poke: Pokemon }) {
  const [showShiny, setShowShiny] = useState(false);
  const bst = Object.values(poke.base_stats).reduce((a, b) => a + b, 0);

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden hover:border-indigo-500 transition-colors">
      <div
        className="h-2"
        style={{ background: TYPE_COLORS[poke.types[0]] ?? "#555" }}
      />
      <div className="p-4">
        <div className="flex items-start justify-between">
          <button className="w-20 h-20 shrink-0" onClick={() => setShowShiny((s) => !s)} title="Toggle shiny">
            <img
              src={showShiny ? poke.sprite_url_shiny : poke.sprite_url}
              alt={poke.name}
              className="w-full h-full object-contain"
            />
          </button>
          <div className="flex-1 pl-3 min-w-0">
            <div className="flex items-baseline justify-between">
              <h3 className="font-bold truncate">{poke.name}</h3>
              <span className="text-xs text-slate-500 font-mono ml-1">#{poke.national_dex}</span>
            </div>
            <div className="flex flex-wrap gap-1 mt-1">
              {poke.types.map((t) => (
                <span
                  key={t}
                  className="text-xs px-2 py-0.5 rounded font-medium text-white"
                  style={{ background: TYPE_COLORS[t] ?? "#555" }}
                >
                  {t}
                </span>
              ))}
            </div>
            <div className="text-xs text-indigo-300 mt-1">{poke.showdown_tier}</div>
            <div className="text-xs text-slate-400">Gen {poke.generation} · BST {bst}</div>
          </div>
        </div>

        <div className="mt-3 space-y-1">
          {(["hp", "atk", "def", "spa", "spd", "spe"] as const).map((s) => (
            <div key={s} className="flex items-center gap-2 text-xs text-slate-400">
              <span className="w-8 uppercase font-medium">{s}</span>
              <StatBar value={poke.base_stats[s]} />
            </div>
          ))}
        </div>

        <div className="mt-3 text-xs text-slate-400 truncate">
          {poke.abilities.join(" / ")}
          {poke.hidden_ability && ` (${poke.hidden_ability})`}
        </div>
      </div>
    </div>
  );
}

export default function PokemonSearchPage() {
  const [search, setSearch] = useState("");
  const [tier, setTier] = useState("");
  const [gen, setGen] = useState(0);

  const { data: pokemon, isLoading } = useQuery({
    queryKey: ["pokemon-list", search, tier, gen],
    queryFn: () =>
      api.pokemon.list({
        search: search || undefined,
        tier: tier || undefined,
        gen: gen || undefined,
      }),
    staleTime: 30_000,
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Pokemon Database</h1>

      <div className="flex flex-wrap gap-3">
        <input
          className="flex-1 min-w-48 bg-slate-800 border border-slate-600 rounded-lg px-4 py-2 text-sm outline-none focus:border-indigo-500"
          placeholder="Search by name…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm outline-none focus:border-indigo-500"
          value={tier}
          onChange={(e) => setTier(e.target.value)}
        >
          {TIERS.map((t) => (
            <option key={t} value={t}>
              {t || "All Tiers"}
            </option>
          ))}
        </select>
        <select
          className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm outline-none focus:border-indigo-500"
          value={gen}
          onChange={(e) => setGen(Number(e.target.value))}
        >
          {GENS.map((g) => (
            <option key={g} value={g}>
              {g === 0 ? "All Gens" : `Gen ${g}`}
            </option>
          ))}
        </select>
      </div>

      {isLoading && (
        <div className="text-slate-400 animate-pulse">Searching…</div>
      )}

      {pokemon && (
        <div className="text-xs text-slate-500">{pokemon.length} results</div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {pokemon?.map((p) => <PokemonCard key={p.national_dex} poke={p} />)}
      </div>
    </div>
  );
}
