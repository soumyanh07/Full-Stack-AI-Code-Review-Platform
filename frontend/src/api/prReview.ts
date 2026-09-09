import api from "./axios";

export interface PRReviewIssue {
  category: string;
  severity: string;
  line: number | null;
  message: string;
  suggestion: string | null;
}

export interface PRFileReview {
  filename: string;
  status: string;
  language: string;
  score: number;
  summary: string;
  issues: PRReviewIssue[];
}

export interface PRReviewResponse {
  owner: string;
  repository: string;
  pr_number: number;
  head_sha: string;
  files_reviewed: number;
  overall_score: number;
  reviews: PRFileReview[];
  github_review: {
    id: number;
    html_url: string;
  } | null;
  github_check: {
    id: number;
    html_url: string;
  } | null;
}

export async function reviewPullRequest(
  owner: string,
  repository: string,
  pullNumber: number,
): Promise<PRReviewResponse> {
  const response = await api.post<PRReviewResponse>(
    "/review/pr",
    {
      owner,
      repository,
      pr_number: pullNumber,
    },
  );

  return response.data;
}