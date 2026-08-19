import { useParams } from "react-router-dom";
import RepositoryChat from "../components/RepositoryChat";

function RepositoryChatPage() {
  const { repositoryId } = useParams<{ repositoryId: string }>();

  const parsedRepositoryId = Number(repositoryId);

  if (!repositoryId || Number.isNaN(parsedRepositoryId)) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-950">
        <p className="text-red-400">Invalid repository ID.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 p-6">
      <RepositoryChat repositoryId={parsedRepositoryId} />
    </div>
  );
}

export default RepositoryChatPage;
