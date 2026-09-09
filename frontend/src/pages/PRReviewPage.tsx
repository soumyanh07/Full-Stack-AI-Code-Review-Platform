import { useState } from "react";
import type { FormEvent } from "react";
import {
  AlertCircle,
  ArrowLeft,
  CheckCircle2,
  ExternalLink,
  FileCode2,
  GitPullRequest,
  Loader2,
  Search,
  ShieldAlert,
  Sparkles,
} from "lucide-react";
import { Link } from "react-router-dom";

import Navbar from "../components/Navbar";
import {
  reviewPullRequest,
  type PRReviewResponse,
} from "../api/prReview";

function PRReviewPage() {
  const [owner, setOwner] = useState("");
  const [repository, setRepository] = useState("");
  const [pullNumber, setPullNumber] = useState("");

  const [result, setResult] = useState<PRReviewResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const parsedPullNumber = Number(pullNumber);

    if (!owner.trim() || !repository.trim() || !pullNumber.trim()) {
      setError("Please enter the owner, repository, and PR number.");
      return;
    }

    if (!Number.isInteger(parsedPullNumber) || parsedPullNumber <= 0) {
      setError("Pull Request number must be a positive integer.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data = await reviewPullRequest(
        owner.trim(),
        repository.trim(),
        parsedPullNumber,
      );

      setResult(data);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to review this Pull Request. Check the repository details and make sure the backend services are running.",
      );
    } finally {
      setLoading(false);
    }
  };

  const scoreClass = (score: number) => {
    if (score >= 8) {
      return "text-emerald-400";
    }

    if (score >= 5) {
      return "text-amber-400";
    }

    return "text-red-400";
  };

  const severityClass = (severity: string) => {
    const normalized = severity.toLowerCase();

    if (normalized === "critical") {
      return "border-red-500/20 bg-red-500/[0.08] text-red-300";
    }

    if (normalized === "high") {
      return "border-orange-500/20 bg-orange-500/[0.08] text-orange-300";
    }

    if (normalized === "medium") {
      return "border-amber-500/20 bg-amber-500/[0.08] text-amber-300";
    }

    return "border-slate-500/20 bg-slate-500/[0.08] text-slate-300";
  };

  return (
    <div className="app-shell min-h-screen text-white">
      <Navbar />

      <main className="lg:ml-64">
        <div className="mx-auto max-w-7xl px-5 py-6 sm:px-8 lg:px-10 lg:py-10">
          <div className="mb-8">
            <Link
              to="/dashboard"
              className="mb-5 inline-flex items-center gap-2 text-sm text-slate-500 transition hover:text-white"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to dashboard
            </Link>

            <div className="mb-3 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.18em] text-indigo-400">
              <Sparkles className="h-3.5 w-3.5" />
              AI Pull Request Review
            </div>

            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Review a Pull Request
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
              Analyze changed files with your local AI review engine and
              publish the review directly to GitHub.
            </p>
          </div>

          <section className="glass mb-8 rounded-3xl p-6 sm:p-8">
            <div className="mb-6 flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-indigo-500/10">
                <GitPullRequest className="h-6 w-6 text-indigo-400" />
              </div>

              <div>
                <h2 className="text-lg font-semibold">
                  Pull Request details
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Enter the GitHub repository and Pull Request you want the AI
                  reviewer to analyze.
                </p>
              </div>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="grid gap-4 md:grid-cols-[1fr_1fr_180px]">
                <div>
                  <label
                    htmlFor="owner"
                    className="mb-2 block text-xs font-medium text-slate-400"
                  >
                    Repository owner
                  </label>

                  <input
                    id="owner"
                    type="text"
                    value={owner}
                    onChange={(event) => setOwner(event.target.value)}
                    placeholder="e.g. octocat"
                    className="w-full rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-indigo-500/50 focus:bg-white/[0.05]"
                  />
                </div>

                <div>
                  <label
                    htmlFor="repository"
                    className="mb-2 block text-xs font-medium text-slate-400"
                  >
                    Repository name
                  </label>

                  <input
                    id="repository"
                    type="text"
                    value={repository}
                    onChange={(event) => setRepository(event.target.value)}
                    placeholder="e.g. hello-world"
                    className="w-full rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-indigo-500/50 focus:bg-white/[0.05]"
                  />
                </div>

                <div>
                  <label
                    htmlFor="pullNumber"
                    className="mb-2 block text-xs font-medium text-slate-400"
                  >
                    PR number
                  </label>

                  <input
                    id="pullNumber"
                    type="number"
                    min="1"
                    value={pullNumber}
                    onChange={(event) => setPullNumber(event.target.value)}
                    placeholder="16"
                    className="w-full rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-indigo-500/50 focus:bg-white/[0.05]"
                  />
                </div>
              </div>

              {error && (
                <div className="mt-5 flex items-start gap-3 rounded-xl border border-red-500/15 bg-red-500/[0.06] p-4">
                  <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-400" />

                  <p className="text-sm leading-6 text-red-300">
                    {error}
                  </p>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="mt-6 inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Reviewing Pull Request...
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4" />
                    Start AI Review
                  </>
                )}
              </button>
            </form>
          </section>

          {loading && (
            <section className="glass rounded-3xl p-10 text-center">
              <Loader2 className="mx-auto h-8 w-8 animate-spin text-indigo-400" />

              <h2 className="mt-4 text-lg font-semibold">
                AI is reviewing the Pull Request
              </h2>

              <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-slate-500">
                The local AI model is analyzing the changed files. This can
                take some time when running on CPU.
              </p>
            </section>
          )}

          {result && !loading && (
            <>
              <section className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <div className="glass rounded-2xl p-5">
                  <p className="text-xs text-slate-500">Overall score</p>

                  <p
                    className={`mt-2 text-3xl font-bold ${scoreClass(
                      result.overall_score,
                    )}`}
                  >
                    {result.overall_score}
                    <span className="text-base text-slate-600">/10</span>
                  </p>
                </div>

                <div className="glass rounded-2xl p-5">
                  <p className="text-xs text-slate-500">Files reviewed</p>

                  <p className="mt-2 text-3xl font-bold">
                    {result.files_reviewed}
                  </p>
                </div>

                <div className="glass rounded-2xl p-5">
                  <p className="text-xs text-slate-500">Pull Request</p>

                  <p className="mt-2 text-3xl font-bold">
                    #{result.pr_number}
                  </p>
                </div>

                <div className="glass rounded-2xl p-5">
                  <p className="text-xs text-slate-500">GitHub review</p>

                  <div className="mt-2 flex items-center gap-2">
                    {result.github_review ? (
                      <>
                        <CheckCircle2 className="h-6 w-6 text-emerald-400" />
                        <span className="font-semibold text-emerald-400">
                          Published
                        </span>
                      </>
                    ) : (
                      <>
                        <AlertCircle className="h-6 w-6 text-amber-400" />
                        <span className="font-semibold text-amber-400">
                          Not published
                        </span>
                      </>
                    )}
                  </div>
                </div>
              </section>

              <section className="glass overflow-hidden rounded-3xl">
                <div className="border-b border-white/[0.06] p-6 sm:p-7">
                  <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
                    <div>
                      <div className="flex items-center gap-2">
                        <FileCode2 className="h-5 w-5 text-indigo-400" />
                        <h2 className="text-lg font-semibold">
                          File-by-file review
                        </h2>
                      </div>

                      <p className="mt-1 text-sm text-slate-500">
                        AI-generated analysis of the changed files.
                      </p>
                    </div>

                    {result.github_review?.html_url && (
                      <a
                        href={result.github_review.html_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-2.5 text-sm font-medium text-slate-300 transition hover:bg-white/[0.06] hover:text-white"
                      >
                        View GitHub review
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    )}
                  </div>
                </div>

                {result.reviews.length === 0 ? (
                  <div className="p-10 text-center">
                    <ShieldAlert className="mx-auto h-8 w-8 text-slate-500" />

                    <h3 className="mt-4 font-semibold">
                      No reviewable files
                    </h3>

                    <p className="mt-2 text-sm text-slate-500">
                      GitHub did not provide source patches for the changed
                      files.
                    </p>
                  </div>
                ) : (
                  <div className="divide-y divide-white/[0.06]">
                    {result.reviews.map((review) => (
                      <article key={review.filename} className="p-6 sm:p-7">
                        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
                          <div className="min-w-0">
                            <div className="flex items-center gap-3">
                              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white/[0.04]">
                                <FileCode2 className="h-5 w-5 text-slate-400" />
                              </div>

                              <div className="min-w-0">
                                <h3 className="truncate font-semibold text-white">
                                  {review.filename}
                                </h3>

                                <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                                  <span>{review.language}</span>
                                  <span>•</span>
                                  <span>{review.status}</span>
                                </div>
                              </div>
                            </div>
                          </div>

                          <div className="shrink-0">
                            <span
                              className={`text-2xl font-bold ${scoreClass(
                                review.score,
                              )}`}
                            >
                              {review.score}
                              <span className="text-sm text-slate-600">
                                /10
                              </span>
                            </span>
                          </div>
                        </div>

                        <p className="mt-5 text-sm leading-7 text-slate-400">
                          {review.summary}
                        </p>

                        {review.issues.length > 0 ? (
                          <div className="mt-6">
                            <div className="mb-3 flex items-center gap-2">
                              <ShieldAlert className="h-4 w-4 text-amber-400" />

                              <h4 className="text-sm font-semibold">
                                Issues detected
                              </h4>

                              <span className="rounded-full bg-white/[0.04] px-2 py-0.5 text-[10px] text-slate-500">
                                {review.issues.length}
                              </span>
                            </div>

                            <div className="space-y-3">
                              {review.issues.map((issue, index) => (
                                <div
                                  key={`${review.filename}-${index}`}
                                  className="rounded-2xl border border-white/[0.06] bg-black/20 p-4"
                                >
                                  <div className="flex flex-wrap items-center gap-2">
                                    <span
                                      className={`rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wide ${severityClass(
                                        issue.severity,
                                      )}`}
                                    >
                                      {issue.severity}
                                    </span>

                                    <span className="rounded-full bg-white/[0.04] px-2.5 py-1 text-[10px] text-slate-500">
                                      {issue.category}
                                    </span>

                                    {issue.line !== null && (
                                      <span className="text-[10px] text-slate-600">
                                        Line {issue.line}
                                      </span>
                                    )}
                                  </div>

                                  <p className="mt-3 text-sm leading-6 text-slate-300">
                                    {issue.message}
                                  </p>

                                  {issue.suggestion && (
                                    <div className="mt-3 rounded-xl border border-indigo-500/10 bg-indigo-500/[0.05] p-3">
                                      <p className="text-xs font-medium text-indigo-300">
                                        Suggestion
                                      </p>

                                      <p className="mt-1 text-sm leading-6 text-slate-400">
                                        {issue.suggestion}
                                      </p>
                                    </div>
                                  )}
                                </div>
                              ))}
                            </div>
                          </div>
                        ) : (
                          <div className="mt-5 flex items-center gap-2 text-sm text-emerald-400">
                            <CheckCircle2 className="h-4 w-4" />
                            No issues detected.
                          </div>
                        )}
                      </article>
                    ))}
                  </div>
                )}
              </section>

              {result.github_check && (
                <section className="mt-6 rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.04] p-5">
                  <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
                    <div>
                      <p className="font-semibold text-emerald-300">
                        GitHub Check Run created
                      </p>

                      <p className="mt-1 text-sm text-slate-500">
                        The AI review result was also published as a GitHub
                        Check Run.
                      </p>
                    </div>

                    <a
                      href={result.github_check.html_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-sm font-medium text-emerald-400 hover:text-emerald-300"
                    >
                      View Check Run
                      <ExternalLink className="h-4 w-4" />
                    </a>
                  </div>
                </section>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}

export default PRReviewPage;