import { useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";
import { useParams, Link } from "react-router-dom";
import {
  ArrowLeft,
  Bot,
  Check,
  Code2,
  Copy,
  GitBranch,
  Loader2,
  Send,
  Sparkles,
  User,
} from "lucide-react";
import Navbar from "../components/Navbar";
import { chatWithRepository } from "../api/chat";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const suggestions = [
  "Explain the architecture of this repository.",
  "Where is authentication implemented?",
  "What are the main services in this project?",
  "Find potential bugs or risky code.",
];

function RepositoryChatPage() {
  const { repositoryId } = useParams<{ repositoryId: string }>();

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const bottomRef = useRef<HTMLDivElement>(null);

  const id = Number(repositoryId);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading || !Number.isFinite(id)) {
      return;
    }

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: trimmedQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await chatWithRepository(id, trimmedQuestion);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.answer,
        },
      ]);
    } catch (error) {
      console.error("Repository chat failed:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I couldn't reach the repository AI service. Please check that the chat service is running and try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const copyMessage = async (content: string, index: number) => {
    await navigator.clipboard.writeText(content);

    setCopiedIndex(index);

    setTimeout(() => {
      setCopiedIndex(null);
    }, 1500);
  };

  if (!repositoryId || !Number.isFinite(id)) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#070b14] text-white">
        <div className="rounded-3xl border border-red-500/20 bg-slate-900 p-8 text-center">
          <h1 className="text-xl font-semibold">Invalid repository</h1>
          <p className="mt-2 text-sm text-slate-500">
            The repository ID is invalid.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell min-h-screen text-white">
      <Navbar />

      <main className="flex min-h-screen flex-col lg:ml-64">
        <header className="border-b border-white/[0.06] bg-slate-950/60 backdrop-blur-xl">
          <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-4 px-5 py-4 sm:px-8">
            <div className="flex min-w-0 items-center gap-3">
              <Link
                to="/dashboard"
                className="rounded-lg p-2 text-slate-500 transition hover:bg-white/[0.05] hover:text-white"
              >
                <ArrowLeft className="h-4 w-4" />
              </Link>

              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-white/[0.05]">
                <GitBranch className="h-4 w-4 text-slate-300" />
              </div>

              <div className="min-w-0">
                <div className="truncate text-sm font-semibold">
                  Repository #{id}
                </div>

                <div className="flex items-center gap-2 text-[11px] text-emerald-400">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                  AI workspace online
                </div>
              </div>
            </div>

            <div className="hidden items-center gap-2 rounded-lg border border-white/[0.06] bg-white/[0.025] px-3 py-2 text-xs text-slate-500 sm:flex">
              <Code2 className="h-3.5 w-3.5" />
              Repository-aware AI
            </div>
          </div>
        </header>

        <div className="mx-auto flex w-full max-w-6xl flex-1 flex-col px-4 py-5 sm:px-8 sm:py-7">
          <div className="mb-5">
            <div className="mb-2 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.16em] text-indigo-400">
              <Sparkles className="h-3.5 w-3.5" />
              AI repository assistant
            </div>

            <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
              Understand your codebase
            </h1>

            <p className="mt-2 text-sm text-slate-500">
              Ask questions about architecture, implementation, bugs, and
              engineering decisions.
            </p>
          </div>

          <div className="glass flex min-h-[620px] flex-1 flex-col overflow-hidden rounded-3xl">
            <div className="flex-1 overflow-y-auto p-4 sm:p-7">
              {messages.length === 0 ? (
                <div className="flex min-h-[500px] items-center justify-center">
                  <div className="w-full max-w-2xl text-center">
                    <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500/20 to-cyan-400/10 ring-1 ring-indigo-400/20">
                      <Bot className="h-8 w-8 text-indigo-300" />
                    </div>

                    <h2 className="mt-6 text-2xl font-semibold">
                      What do you want to understand?
                    </h2>

                    <p className="mx-auto mt-3 max-w-lg text-sm leading-6 text-slate-500">
                      Ask your AI assistant about the repository. It can help
                      explain architecture, implementation details, and
                      potential problems.
                    </p>

                    <div className="mt-8 grid gap-2 sm:grid-cols-2">
                      {suggestions.map((suggestion) => (
                        <button
                          key={suggestion}
                          onClick={() => setQuestion(suggestion)}
                          className="rounded-xl border border-white/[0.07] bg-white/[0.025] p-3 text-left text-xs text-slate-400 transition hover:border-indigo-500/25 hover:bg-indigo-500/[0.04] hover:text-slate-200"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  {messages.map((message, index) => {
                    const isUser = message.role === "user";

                    return (
                      <div
                        key={`${message.role}-${index}`}
                        className={`flex gap-3 ${
                          isUser ? "justify-end" : "justify-start"
                        }`}
                      >
                        {!isUser && (
                          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-500">
                            <Bot className="h-4 w-4 text-white" />
                          </div>
                        )}

                        <div
                          className={`group relative max-w-[85%] rounded-2xl px-4 py-3 sm:max-w-[75%] ${
                            isUser
                              ? "bg-indigo-500 text-white"
                              : "border border-white/[0.06] bg-white/[0.035] text-slate-300"
                          }`}
                        >
                          <div className="whitespace-pre-wrap text-sm leading-7">
                            {message.content}
                          </div>

                          {!isUser && (
                            <button
                              onClick={() =>
                                copyMessage(message.content, index)
                              }
                              className="absolute -right-2 -top-2 rounded-lg border border-white/[0.08] bg-slate-900 p-1.5 text-slate-500 opacity-0 shadow-xl transition group-hover:opacity-100 hover:text-white"
                              title="Copy"
                            >
                              {copiedIndex === index ? (
                                <Check className="h-3.5 w-3.5 text-emerald-400" />
                              ) : (
                                <Copy className="h-3.5 w-3.5" />
                              )}
                            </button>
                          )}
                        </div>

                        {isUser && (
                          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-800 ring-1 ring-white/[0.06]">
                            <User className="h-4 w-4 text-slate-300" />
                          </div>
                        )}
                      </div>
                    );
                  })}

                  {loading && (
                    <div className="flex gap-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-500">
                        <Bot className="h-4 w-4 text-white" />
                      </div>

                      <div className="flex items-center gap-2 rounded-2xl border border-white/[0.06] bg-white/[0.035] px-4 py-3">
                        <Loader2 className="h-4 w-4 animate-spin text-indigo-400" />
                        <span className="text-xs text-slate-500">
                          Analyzing repository...
                        </span>
                      </div>
                    </div>
                  )}

                  <div ref={bottomRef} />
                </div>
              )}
            </div>

            <div className="border-t border-white/[0.06] bg-slate-950/50 p-3 sm:p-4">
              <form onSubmit={handleSubmit}>
                <div className="flex items-end gap-2 rounded-2xl border border-white/[0.08] bg-white/[0.025] p-2 transition focus-within:border-indigo-500/30">
                  <textarea
                    value={question}
                    onChange={(event) => setQuestion(event.target.value)}
                    disabled={loading}
                    rows={1}
                    placeholder="Ask about this repository..."
                    className="max-h-32 min-h-11 flex-1 resize-none bg-transparent px-3 py-3 text-sm text-white outline-none placeholder:text-slate-600"
                    onKeyDown={(event) => {
                      if (event.key === "Enter" && !event.shiftKey) {
                        event.preventDefault();
                        event.currentTarget.form?.requestSubmit();
                      }
                    }}
                  />

                  <button
                    type="submit"
                    disabled={loading || !question.trim()}
                    className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-indigo-500 text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-30"
                  >
                    {loading ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Send className="h-4 w-4" />
                    )}
                  </button>
                </div>

                <p className="mt-2 px-2 text-[10px] text-slate-700">
                  Enter to send · Shift + Enter for a new line
                </p>
              </form>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default RepositoryChatPage;

