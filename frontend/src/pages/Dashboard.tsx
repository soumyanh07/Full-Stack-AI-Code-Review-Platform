import { useEffect, useState } from "react";
import { getRepositories } from "../api/repositories";
import type { Repository } from "../api/repositories";

function Dashboard() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRepositories() {
      try {
        setLoading(true);
        setError("");

        const data = await getRepositories();

        setRepositories(data);
      } catch (err) {
        console.error("Failed to load repositories:", err);
        setError("Unable to load repositories.");
      } finally {
        setLoading(false);
      }
    }

    loadRepositories();
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-10">
          <h1 className="text-4xl font-bold">
            AI Code Review Dashboard
          </h1>

          <p className="mt-2 text-gray-400">
            Manage your repositories and review code with AI.
          </p>
        </div>

        {loading && (
          <div className="rounded-lg border border-gray-700 bg-gray-800 p-8 text-center">
            <p className="text-gray-400">
              Loading repositories...
            </p>
          </div>
        )}

        {!loading && error && (
          <div className="rounded-lg border border-red-800 bg-red-950 p-6">
            <p className="text-red-300">
              {error}
            </p>

            <p className="mt-2 text-sm text-gray-400">
              Make sure the repository service is running.
            </p>
          </div>
        )}

        {!loading && !error && repositories.length === 0 && (
          <div className="rounded-lg border border-gray-700 bg-gray-800 p-8 text-center">
            <h2 className="text-xl font-semibold">
              No repositories found
            </h2>

            <p className="mt-2 text-gray-400">
              Add a repository to get started.
            </p>
          </div>
        )}

        {!loading && !error && repositories.length > 0 && (
          <>
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-2xl font-semibold">
                Your Repositories
              </h2>

              <span className="rounded-full bg-gray-800 px-4 py-2 text-sm text-gray-300">
                {repositories.length} repositories
              </span>
            </div>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {repositories.map((repository) => (
                <div
                  key={repository.id}
                  className="rounded-xl border border-gray-700 bg-gray-800 p-6 transition hover:border-gray-500 hover:bg-gray-750"
                >
                  <div className="mb-4">
                    <h3 className="text-xl font-semibold">
                      {repository.name}
                    </h3>

                    <p className="mt-1 text-sm text-gray-500">
                      Repository #{repository.id}
                    </p>
                  </div>

                  <p className="mb-5 break-all text-sm text-gray-400">
                    {repository.url}
                  </p>

                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      Indexed repository
                    </span>

                    <a
                      href={repository.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium transition hover:bg-blue-500"
                    >
                      GitHub
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
