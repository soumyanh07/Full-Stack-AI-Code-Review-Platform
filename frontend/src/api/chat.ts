import api from "./axios";

export interface ChatRequest {
  repository_id: number;
  question: string;
}

export interface ChatResponse {
  repository_id: number;
  question: string;
  answer: string;
  context: string;
}

export async function chatWithRepository(
  repositoryId: number,
  question: string,
): Promise<ChatResponse> {
  const response = await api.post<ChatResponse>("/chat", {
    repository_id: repositoryId,
    question,
  });

  return response.data;
}