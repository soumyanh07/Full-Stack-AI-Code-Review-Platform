import { useState } from "react";
import type { FormEvent } from "react";
import { Send, Bot, User, Loader2 } from "lucide-react";
import { chatWithRepository } from "../api/chat";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface RepositoryChatProps {
  repositoryId: number;
}

function RepositoryChat({ repositoryId }: RepositoryChatProps) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
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
      const response = await chatWithRepository(
        repositoryId,
        trimmedQuestion
      );

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
            "Unable to get an answer. Please make sure the repository service is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-[calc(100vh-140px)] flex-col rounded-2xl border border-gray-800 bg-gray-900">
      <div className="border-b border-gray-800 px-6 py-4">
        <h2 className="text-xl font-semibold text-white">
          Chat with Repository
        </h2>

        <p className="mt-1 text-sm text-gray-400">
          Ask questions about the indexed codebase.
        </p>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto p-6">
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center text-center">
            <div>
              <Bot className="mx-auto mb-3 h-10 w-10 text-gray-500" />

              <p className="text-gray-400">
                Ask a question about this repository.
              </p>

              <p className="mt-2 text-sm text-gray-600">
                Example: What is FastAPI and how is the main application
                created?
              </p>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-3 ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {message.role === "assistant" && (
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-600">
                <Bot className="h-4 w-4 text-white" />
              </div>
            )}

            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-6 ${
                message.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-800 text-gray-200"
              }`}
            >
              <div className="whitespace-pre-wrap">
                {message.content}
              </div>
            </div>

            {message.role === "user" && (
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gray-700">
                <User className="h-4 w-4 text-gray-200" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-600">
              <Bot className="h-4 w-4 text-white" />
            </div>

            <div className="rounded-2xl bg-gray-800 px-4 py-3">
              <Loader2 className="h-5 w-5 animate-spin text-gray-400" />
            </div>
          </div>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        className="border-t border-gray-800 p-4"
      >
        <div className="flex gap-3">
          <input
            type="text"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask something about the repository..."
            disabled={loading}
            className="flex-1 rounded-xl border border-gray-700 bg-gray-800 px-4 py-3 text-sm text-white outline-none placeholder:text-gray-500 focus:border-blue-500"
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="flex items-center justify-center rounded-xl bg-blue-600 px-5 py-3 text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </button>
        </div>
      </form>
    </div>
  );
}

export default RepositoryChat;
