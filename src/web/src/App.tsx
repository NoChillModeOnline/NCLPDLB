import { Routes, Route, NavLink } from "react-router-dom";
import DraftBoardPage from "./pages/DraftBoardPage";
import StandingsPage from "./pages/StandingsPage";
import TeamsPage from "./pages/TeamsPage";
import SchedulePage from "./pages/SchedulePage";
import PokemonSearchPage from "./pages/PokemonSearchPage";

function Nav() {
  const base = "px-4 py-2 rounded-md text-sm font-medium transition-colors";
  const active = "bg-indigo-600 text-white";
  const inactive = "text-slate-300 hover:bg-slate-700";
  return (
    <nav className="bg-slate-900 border-b border-slate-700 px-6 py-3 flex items-center gap-2">
      <span className="text-lg font-bold text-indigo-400 mr-6">⚔️ Draft League</span>
      {[
        { to: "/", label: "Draft Board" },
        { to: "/standings", label: "Standings" },
        { to: "/teams", label: "Teams" },
        { to: "/schedule", label: "Schedule" },
        { to: "/pokemon", label: "Pokemon" },
      ].map(({ to, label }) => (
        <NavLink
          key={to}
          to={to}
          end={to === "/"}
          className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
        >
          {label}
        </NavLink>
      ))}
    </nav>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Nav />
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        <Routes>
          <Route path="/" element={<DraftBoardPage />} />
          <Route path="/standings" element={<StandingsPage />} />
          <Route path="/teams" element={<TeamsPage />} />
          <Route path="/schedule" element={<SchedulePage />} />
          <Route path="/pokemon" element={<PokemonSearchPage />} />
        </Routes>
      </main>
    </div>
  );
}
