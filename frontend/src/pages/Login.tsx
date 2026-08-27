import { useState } from "react";
import type { FormEvent } from "react";
import {
  ArrowRight,
  Bot,
  CheckCircle2,
  Code2,
  Eye,
  EyeOff,
  GitBranch,
  LockKeyhole,
  Mail,
  Sparkles,
} from "lucide-react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuthStore } from "../store/authStore";

function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const login = useAuthStore((state) => state.login);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (event: FormEvent) => {
    event.preventDefault();

    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const response = await api.post("/auth/login", {
        email,
        password,
      });

      login(response.data.access_token, {
        id: response.data.user?.id ?? 0,
        email: response.data.user?.email ?? email,
      });

      const destination =
        (location.state as { from?: string } | null)?.from ||
        "/dashboard";

      navigate(destination, { replace: true });
    } catch (err: any) {
      console.error(err);

      setError(
        err?.response?.data?.detail ||
          "Login failed. Check your credentials and try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid-pattern relative min-h-screen overflow-hidden bg-[#070b14] text-white">
      <div className="absolute -left-32 -top-32 h-96 w-96 rounded-full bg-indigo-600/15 blur-3xl" />
      <div className="absolute -bottom-40 -right-32 h-96 w-96 rounded-full bg-cyan-500/10 blur-3xl" />

      <div className="relative mx-auto flex min-h-screen max-w-7xl items-center px-6 py-10 lg:px-10">
        <div className="grid w-full overflow-hidden rounded-3xl border border-white/[0.08] bg-slate-950/70 shadow-2xl shadow-black/40 backdrop-blur-xl lg:grid-cols-2">
          <div className="hidden min-h-[680px] flex-col justify-between border-r border-white/[0.07] bg-gradient-to-br from-indigo-950/40 via-slate-950 to-cyan-950/20 p-12 lg:flex">
            <div>
              <div className="mb-16 flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400">
                  <Sparkles className="h-5 w-5" />
                </div>

                <div className="text-lg font-bold">
                  Code<span className="text-indigo-400">Pilot</span>
                </div>
              </div>

              <div className="max-w-lg">
                <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-indigo-400/20 bg-indigo-400/10 px-3 py-1.5 text-xs font-medium text-indigo-300">
                  <Sparkles className="h-3.5 w-3.5" />
                  AI-powered engineering
                </div>

                <h1 className="text-5xl font-bold leading-[1.08] tracking-tight">
                  Ship better code.
                  <span className="gradient-text block">
                    Review smarter.
                  </span>
                </h1>

                <p className="mt-6 text-base leading-7 text-slate-400">
                  Analyze repositories, understand complex codebases, and
                  collaborate with an AI engineering assistant.
                </p>
              </div>
            </div>

            <div className="space-y-3">
              {[
                "AI-powered code review",
                "Repository-aware conversations",
                "Developer-focused insights",
              ].map((item) => (
                <div
                  key={item}
                  className="flex items-center gap-3 text-sm text-slate-300"
                >
                  <CheckCircle2 className="h-4 w-4 text-cyan-400" />
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div className="flex items-center p-7 sm:p-10 lg:p-12">
            <div className="mx-auto w-full max-w-md">
              <div className="mb-8 lg:hidden">
                <div className="mb-5 flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400">
                    <Sparkles className="h-5 w-5" />
                  </div>
                  <div className="font-bold">
                    Code<span className="text-indigo-400">Pilot</span>
                  </div>
                </div>
              </div>

              <div className="mb-8">
                <h2 className="text-3xl font-bold tracking-tight">
                  Welcome back
                </h2>
                <p className="mt-2 text-sm text-slate-500">
                  Sign in to continue to your engineering workspace.
                </p>
              </div>

              {error && (
                <div className="mb-5 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                  {error}
                </div>
              )}

              <button
                type="button"
                className="mb-5 flex w-full items-center justify-center gap-3 rounded-xl border border-white/10 bg-white/[0.04] px-4 py-3 text-sm font-medium text-slate-200 transition hover:bg-white/[0.07]"
              >
                <GitBranch className="h-4 w-4" />
                Continue with GitBranch
              </button>

              <div className="mb-5 flex items-center gap-3">
                <div className="h-px flex-1 bg-white/[0.07]" />
                <span className="text-xs text-slate-600">OR</span>
                <div className="h-px flex-1 bg-white/[0.07]" />
              </div>

              <form onSubmit={handleLogin} className="space-y-5">
                <label className="block">
                  <span className="mb-2 block text-xs font-medium text-slate-400">
                    Email address
                  </span>

                  <div className="relative">
                    <Mail className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600" />

                    <input
                      type="email"
                      value={email}
                      onChange={(event) => setEmail(event.target.value)}
                      placeholder="you@example.com"
                      className="w-full rounded-xl border border-white/[0.08] bg-white/[0.035] py-3 pl-10 pr-4 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-indigo-500/60 focus:bg-white/[0.05]"
                    />
                  </div>
                </label>

                <label className="block">
                  <span className="mb-2 block text-xs font-medium text-slate-400">
                    Password
                  </span>

                  <div className="relative">
                    <LockKeyhole className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-600" />

                    <input
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(event) => setPassword(event.target.value)}
                      placeholder="Enter your password"
                      className="w-full rounded-xl border border-white/[0.08] bg-white/[0.035] py-3 pl-10 pr-11 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-indigo-500/60 focus:bg-white/[0.05]"
                    />

                    <button
                      type="button"
                      onClick={() => setShowPassword((value) => !value)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-600 hover:text-slate-300"
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </button>
                  </div>
                </label>

                <button
                  disabled={loading}
                  className="group flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:from-indigo-400 hover:to-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? "Signing in..." : "Sign in"}
                  {!loading && (
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-0.5" />
                  )}
                </button>
              </form>

              <p className="mt-7 text-center text-sm text-slate-500">
                Don't have an account?{" "}
                <Link
                  to="/register"
                  className="font-medium text-indigo-400 hover:text-indigo-300"
                >
                  Create one
                </Link>
              </p>

              <div className="mt-8 flex justify-center gap-6 text-[11px] text-slate-700">
                <span className="flex items-center gap-1">
                  <Code2 className="h-3 w-3" />
                  Developer-first
                </span>
                <span className="flex items-center gap-1">
                  <Bot className="h-3 w-3" />
                  AI assisted
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;

