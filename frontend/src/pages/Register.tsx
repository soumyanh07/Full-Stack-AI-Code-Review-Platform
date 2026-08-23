import { useState } from "react";
import type { FormEvent } from "react";
import {
  ArrowRight,
  CheckCircle2,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  Sparkles,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/axios";

function Register() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async (event: FormEvent) => {
    event.preventDefault();

    if (!email || !password) {
      setError("Please complete all fields.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      await api.post("/auth/register", {
        username: email.split("@")[0],
        email,
        password,
      });

      navigate("/login");
    } catch (err: any) {
      console.error(err);

      setError(
        err?.response?.data?.detail ||
          "Registration failed. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid-pattern min-h-screen bg-[#070b14] px-6 py-10 text-white">
      <div className="mx-auto flex min-h-[calc(100vh-5rem)] max-w-5xl items-center">
        <div className="grid w-full overflow-hidden rounded-3xl border border-white/[0.08] bg-slate-950/80 shadow-2xl shadow-black/40 backdrop-blur-xl lg:grid-cols-[0.9fr_1.1fr]">
          <div className="hidden flex-col justify-between bg-gradient-to-br from-cyan-950/30 via-slate-950 to-indigo-950/40 p-10 lg:flex">
            <div>
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400">
                  <Sparkles className="h-5 w-5" />
                </div>
                <span className="font-bold">
                  Code<span className="text-indigo-400">Pilot</span>
                </span>
              </div>

              <h1 className="mt-20 text-4xl font-bold leading-tight">
                Your AI pair programmer,
                <span className="gradient-text block">
                  built for real codebases.
                </span>
              </h1>

              <p className="mt-5 text-sm leading-6 text-slate-400">
                Explore repositories, understand architecture, and get
                actionable engineering feedback from AI.
              </p>
            </div>

            <div className="space-y-3">
              {[
                "Repository-aware AI",
                "Fast developer workflows",
                "Built for modern engineering teams",
              ].map((item) => (
                <div
                  key={item}
                  className="flex items-center gap-2 text-sm text-slate-300"
                >
                  <CheckCircle2 className="h-4 w-4 text-cyan-400" />
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div className="p-7 sm:p-10">
            <div className="mx-auto max-w-md">
              <div className="mb-8">
                <h2 className="text-3xl font-bold">Create your account</h2>
                <p className="mt-2 text-sm text-slate-500">
                  Start building with an AI engineering assistant.
                </p>
              </div>

              {error && (
                <div className="mb-5 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                  {error}
                </div>
              )}

              <form onSubmit={handleRegister} className="space-y-5">
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
                      className="w-full rounded-xl border border-white/[0.08] bg-white/[0.035] py-3 pl-10 pr-4 text-sm outline-none placeholder:text-slate-700 focus:border-indigo-500/60"
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
                      placeholder="Create a strong password"
                      className="w-full rounded-xl border border-white/[0.08] bg-white/[0.035] py-3 pl-10 pr-11 text-sm outline-none placeholder:text-slate-700 focus:border-indigo-500/60"
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
                  className="group flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-600 py-3 text-sm font-semibold shadow-lg shadow-indigo-600/20 transition hover:from-indigo-400 hover:to-indigo-500 disabled:opacity-50"
                >
                  {loading ? "Creating account..." : "Create account"}

                  {!loading && (
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-0.5" />
                  )}
                </button>
              </form>

              <p className="mt-7 text-center text-sm text-slate-500">
                Already have an account?{" "}
                <Link
                  to="/login"
                  className="font-medium text-indigo-400 hover:text-indigo-300"
                >
                  Sign in
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;

