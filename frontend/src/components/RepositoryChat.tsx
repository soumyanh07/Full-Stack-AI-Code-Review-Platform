import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export interface ChatResponse {
  repository_id: number;
  question: string;
  answer: string;
  context?: string;
}

export async function chatWithRepository(
  repositoryId: number,
  question: string
): Promise<ChatResponse> {
  const response = await axios.post<ChatResponse>(
    `${API_BASE_URL}/api/v1/chat`,
    {
      repository_id: repositoryId,
      question,
    }
  );

  return response.data;
}