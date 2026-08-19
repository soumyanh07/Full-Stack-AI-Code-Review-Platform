import api from "./axios";

export interface Repository {
  id: number;
  name: string;
  url: string;
  local_path: string;
}

export async function getRepositories(): Promise<Repository[]> {
  const response = await api.get<Repository[]>("/repositories");

  return response.data;
}
