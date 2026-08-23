import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowUpRight,
  Bot,
  ExternalLink,
  FolderGit2,
  GitBranch,
  Loader2,
  RefreshCw,
  Sparkles,
  Terminal,
} from "lucide-react";
import Navbar from "../components/Navbar";
import { getRepositories } from "../api/repositories";
import type { Repository } from "../api/repositories";
import { useAuthStore } from "../store/authStore";

function Dashboard() {
  const user = useAuthStore((state) => state.user);

  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadRepositories = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getRepositories();
      setRepositories(data);
    } catch (err) {
      console.error(err);
      setError("Unable to load repositories.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRepositories();
  }, []);

  return (
    <div className="app-shell min-h-screen text-white">
      <Navbar />

      <main className="lg:ml-64">
        <div className="mx-auto max-w-7xl px-5 py-6 sm:px-8 lg:px-10 lg:py-10">
          <header className="mb-10 flex flex-col justify-between gap-5 md:flex-row md:items-end">
            <div>
              <div className="mb-3 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.18em] text-indigo-400">
                <Sparkles className="h-3.5 w-3.5" />
                Engineering workspace
              </div>

              <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
                Good to see you,{" "}
                <span className="gradient-text">
                  {user?.email?.split("@")[0] || "developer"}
                </span>
              </h1>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
                Review code, explore repositories, and collaborate with your
                AI engineering assistant.
              </p>
            </div>

            <button
              onClick={loadRepositories}
              disabled={loading}
              className="flex items-center justify-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-2.5 text-sm font-medium text-slate-300 transition hover:bg-white/[0.06] disabled:opacity-50"
            >
              <RefreshCw
                className={`h-4 w-4 ${loading ? "animate-spin" : ""}`}
              />
              Refresh
            </button>
          </header>

          <section className="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {[
              {
                label: "Repositories",
                value: repositories.length,
                icon: FolderGit2,
                accent: "text-indigo-400",
              },
              {
                label: "AI Reviews",
                value: "Ready",
                icon: Bot,
                accent: "text-cyan-400",
              },
              {
                label: "AI Chat",
                value: "Online",
                icon: Sparkles,
                accent: "text-violet-400",
              },
              {
                label: "Workspace",
                value: "Active",
                icon: Terminal,
                accent: "text-emerald-400",
              },
            ].map((stat) => {
              const Icon = stat.icon;

              return (
                <div
                  key={stat.label}
                  className="glass glass-hover rounded-2xl p-5"
                >
                  <div className="mb-4 flex items-center justify-between">
                    <div className="rounded-xl bg-white/[0.04] p-2.5">
                      <Icon className={`h-5 w-5 ${stat.accent}`} />
                    </div>
                  </div>

                  <p className="text-xs text-slate-500">{stat.label}</p>
                  <p className="mt-1 text-xl font-semibold">{stat.value}</p>
                </div>
              );
            })}
          </section>

          <section className="glass mb-8 overflow-hidden rounded-3xl">
            <div className="border-b border-white/[0.06] p-6 sm:p-7">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <FolderGit2 className="h-5 w-5 text-indigo-400" />
                    <h2 className="text-lg font-semibold">
                      Your repositories
                    </h2>
                  </div>

                  <p className="mt-1 text-sm text-slate-500">
                    Connected codebases available for AI analysis.
                  </p>
                </div>

                <span className="rounded-full border border-white/[0.07] bg-white/[0.03] px-3 py-1 text-xs text-slate-400">
                  {repositories.length} total
                </span>
              </div>
            </div>

            {loading && (
              <div className="p-12 text-center">
                <Loader2 className="mx-auto h-7 w-7 animate-spin text-indigo-400" />
                <p className="mt-3 text-sm text-slate-500">
                  Loading repositories...
                </p>
              </div>
            )}

            {!loading && error && (
              <div className="m-6 rounded-2xl border border-red-500/15 bg-red-500/[0.06] p-6">
                <p className="font-medium text-red-300">{error}</p>
                <button
                  onClick={loadRepositories}
                  className="mt-4 rounded-lg bg-red-500/10 px-3 py-2 text-xs text-red-300 hover:bg-red-500/20"
                >
                  Try again
                </button>
              </div>
            )}

            {!loading && !error && repositories.length === 0 && (
              <div className="p-12 text-center">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-white/[0.04]">
                  <GitBranch className="h-7 w-7 text-slate-500" />
                </div>

                <h3 className="mt-5 text-lg font-semibold">
                  No repositories yet
                </h3>

                <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
                  Connect a repository to start using AI-powered code review
                  and repository chat.
                </p>
              </div>
            )}

            {!loading && !error && repositories.length > 0 && (
              <div className="grid gap-4 p-5 sm:p-6 lg:grid-cols-2">
                {repositories.map((repository) => (
                  <article
                    key={repository.id}
                    className="group rounded-2xl border border-white/[0.07] bg-white/[0.02] p-5 transition hover:border-indigo-500/25 hover:bg-indigo-500/[0.025]"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex min-w-0 items-center gap-3">
                        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-slate-800 to-slate-900 ring-1 ring-white/[0.08]">
                          <GitBranch className="h-5 w-5 text-slate-300" />
                        </div>

                        <div className="min-w-0">
                          <h3 className="truncate font-semibold text-white">
                            {repository.name}
                          </h3>

                          <div className="mt-1 flex items-center gap-2 text-xs text-slate-600">
                            <GitBranch className="h-3 w-3" />
                            Repository #{repository.id}
                          </div>
                        </div>
                      </div>

                      <span className="rounded-full bg-emerald-500/10 px-2.5 py-1 text-[10px] font-medium uppercase tracking-wide text-emerald-400">
                        Connected
                      </span>
                    </div>

                    <p className="mt-5 truncate rounded-lg bg-black/20 px-3 py-2 text-xs text-slate-500">
                      {repository.url}
                    </p>

                    <div className="mt-5 flex gap-2">
                      <Link
                        to={`/repositories/${repository.id}/chat`}
                        className="group/button flex flex-1 items-center justify-center gap-2 rounded-xl bg-indigo-500 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-400"
                      >
                        <Bot className="h-4 w-4" />
                        Open AI Chat
                        <ArrowUpRight className="h-3.5 w-3.5 transition group-hover/button:translate-x-0.5 group-hover/button:-translate-y-0.5" />
                      </Link>

                      <a
                        href={repository.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center justify-center rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 text-slate-400 transition hover:bg-white/[0.06] hover:text-white"
                        title="Open GitBranch"
                      >
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>

          <section className="grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-indigo-500/10 bg-gradient-to-br from-indigo-500/[0.08] to-transparent p-6">
              <Sparkles className="h-6 w-6 text-indigo-400" />

              <h3 className="mt-4 font-semibold">
                AI code review is ready
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-500">
                Your AI service can analyze code and return structured
                engineering feedback.
              </p>
            </div>

            <div className="rounded-2xl border border-cyan-500/10 bg-gradient-to-br from-cyan-500/[0.07] to-transparent p-6">
              <Bot className="h-6 w-6 text-cyan-400" />

              <h3 className="mt-4 font-semibold">
                Ask your codebase
              </h3>

              <p className="mt-2 text-sm leading-6 text-slate-500">
                Use repository-aware chat to understand architecture and
                implementation details.
              </p>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;

