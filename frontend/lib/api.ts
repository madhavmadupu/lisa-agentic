export const API_BASE_URL = "http://localhost:8000";

export interface AgentRequest {
  user_request: string;
  architect_model?: string;
  coder_model?: string;
  reviewer_model?: string;
}

export interface SessionResponse {
  session_id: string;
}

export interface FileNode {
  path: string;
  name: string;
  type: 'file' | 'directory';
  children?: FileNode[];
}

export async function startAgentRun(request: AgentRequest): Promise<SessionResponse> {
  const response = await fetch(`${API_BASE_URL}/api/agent/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Failed to start agent run: ${response.statusText}`);
  }

  return response.json();
}

export async function getWorkspaceFiles(): Promise<{ files: string[] }> {
  const response = await fetch(`${API_BASE_URL}/api/workspace/files`);
  if (!response.ok) {
    throw new Error("Failed to fetch workspace files");
  }
  return response.json();
}

export async function getFileContent(path: string): Promise<{ content: string }> {
  const response = await fetch(`${API_BASE_URL}/api/workspace/file?path=${encodeURIComponent(path)}`);
  if (!response.ok) {
     const errorText = await response.text();
     throw new Error(errorText || "Failed to read file");
  }
  return response.json();
}
