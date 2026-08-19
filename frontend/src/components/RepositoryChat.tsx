import { FormEvent, useState } from "react";
import { Send, Bot, User, Loader2 } from "lucide-react";
import { chatWithRepository } from "../api/chat";

interface RepositoryChatProps {
  repositoryId: number;
}

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function RepositoryChat({
  repositoryId,
}: RepositoryChatProps) {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState<Message[]>([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    setError("");

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: trimmedQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await chatWithRepository(
        repositoryId,
        trimmedQuestion,
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: response.answer,
        },
      ]);
    } catch (err) {
      console.error("Repository chat failed:", err);

      setError(
        "Unable to get an answer. Please make sure the repository service is running.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mx-auto mt-8 w-full max-w-4xl rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div className="border-b border-gray-200 px-6 py-5">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-indigo-100 p-2">
            <Bot className="h-5 w-5 text-indigo-600" />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              Chat with Repository
            </h2>

            <p className="text-sm text-gray-500">
              Ask questions about the indexed codebase.
            </p>
          </div>
        </div>
      </div>

      <div className="min-h-[350px] max-h-[500px] space-y-4 overflow-y-auto p-6">
        {messages.length === 0 && (
          <div className="flex min-h-[280px] items-center justify-center text-center">
            <div>
              <Bot className="mx-auto mb-4 h-10 w-10 text-gray-400" />

              <h3 className="font-medium text-gray-700">
                Ask about this repository
              </h3>

              <p className="mt-2 max-w-md text-sm text-gray-500">
                Try asking about the architecture, files, functions,
                dependencies, or implementation details.
              </p>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-3 ${
              message.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >
            {message.role === "assistant" && (
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-indigo-100">
                <Bot className="h-4 w-4 text-indigo-600" />
              </div>
            )}

            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-6 ${
                message.role === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-gray-100 text-gray-800"
              }`}
            >
              {message.content}
            </div>

            {message.role === "user" && (
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gray-200">
                <User className="h-4 w-4 text-gray-600" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-100">
              <Bot className="h-4 w-4 text-indigo-600" />
            </div>

            <div className="flex items-center gap-2 rounded-2xl bg-gray-100 px-4 py-3 text-sm text-gray-600">
              <Loader2 className="h-4 w-4 animate-spin" />
              Thinking...
            </div>
          </div>
        )}

        {error && (
          <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        className="border-t border-gray-200 p-4"
      >
        <div className="flex gap-3">
          <input
            type="text"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask something about this repository..."
            disabled={loading}
            className="flex-1 rounded-xl border border-gray-300 px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-gray-100"
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="flex items-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Send className="h-4 w-4" />
            Ask
          </button>
        </div>
      </form>
    </section>
  );
}