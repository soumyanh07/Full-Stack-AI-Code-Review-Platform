import {
  Bot,
  LayoutDashboard,
  LogOut,
  Sparkles,
} from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

function Navbar() {
  const navigate = useNavigate();
  const logout = useAuthStore((state) => state.logout);
  const user = useAuthStore((state) => state.user);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const navClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
      isActive
        ? "bg-indigo-500/15 text-indigo-300 ring-1 ring-indigo-500/20"
        : "text-slate-400 hover:bg-white/[0.04] hover:text-white"
    }`;

  return (
    <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 border-r border-white/[0.07] bg-slate-950/80 px-4 py-5 backdrop-blur-xl lg:flex lg:flex-col">
      <div className="mb-8 flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 shadow-lg shadow-indigo-500/20">
          <Sparkles className="h-5 w-5 text-white" />
        </div>

        <div>
          <div className="font-bold tracking-tight text-white">
            Code<span className="text-indigo-400">Pilot</span>
          </div>

          <div className="text-[10px] uppercase tracking-[0.18em] text-slate-500">
            AI Engineering
          </div>
        </div>
      </div>

      <div className="mb-3 px-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-600">
        Workspace
      </div>

      <nav className="space-y-1">
        <NavLink to="/dashboard" className={navClass}>
          <LayoutDashboard className="h-4 w-4" />
          Dashboard
        </NavLink>
      </nav>

      <div className="mt-auto">
        <div className="mb-3 rounded-2xl border border-indigo-500/10 bg-indigo-500/[0.06] p-4">
          <div className="mb-2 flex items-center gap-2 text-sm font-medium text-white">
            <Bot className="h-4 w-4 text-cyan-400" />
            AI Review Engine
          </div>

          <p className="text-xs leading-5 text-slate-500">
            Your repositories are ready for intelligent code analysis.
          </p>
        </div>

        <div className="flex items-center gap-3 border-t border-white/[0.06] pt-4">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-indigo-400 to-cyan-400 text-sm font-bold text-white">
            {user?.email?.charAt(0).toUpperCase() || "U"}
          </div>

          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-white">
              {user?.email || "Developer"}
            </p>
            <p className="text-xs text-slate-500">Developer account</p>
          </div>

          <button
            onClick={handleLogout}
            title="Logout"
            className="rounded-lg p-2 text-slate-500 transition hover:bg-white/[0.05] hover:text-red-400"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}

export default Navbar;