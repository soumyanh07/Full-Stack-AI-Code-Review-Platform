import { useParams } from "react-router-dom";
import RepositoryChat from "../components/RepositoryChat";

export default function RepositoryChatPage() {
  const { repositoryId } = useParams<{ repositoryId: string }>();

  const parsedRepositoryId = Number(repositoryId);

  if (!repositoryId || Number.isNaN(parsedRepositoryId)) {
    return (
      <div className="p-6 text-center text-red-600">
        Invalid repository ID.
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 px-4 py-8">
      <RepositoryChat repositoryId={parsedRepositoryId} />
    </div>
  );
}
