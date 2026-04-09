const BASE_URL = (process.env.EXPO_PUBLIC_API_URL ?? 'https://ai-recruiter-d5bg.onrender.com').replace(/\/$/, '');

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed with ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export type Job = {
  id: string;
  title: string;
  description: string;
  required_skills: string[];
  min_experience_years: number;
};

export type Candidate = {
  id: string;
  full_name: string;
  email: string;
  final_score: number;
  recommendation: string;
};

export type Ranking = {
  candidate_id: string;
  name: string;
  email: string;
  final_score: number;
  recommendation: string;
};

export type ResumeUploadFile = {
  uri: string;
  name: string;
  type?: string;
};

export const api = {
  listJobs: () => request<Job[]>('/api/jobs'),
  createJob: (body: Omit<Job, 'id'>) => request<Job>('/api/jobs', { method: 'POST', body: JSON.stringify(body) }),
  createCandidate: (body: { full_name: string; email: string; target_job_id?: string }) =>
    request<Candidate>('/api/candidates', { method: 'POST', body: JSON.stringify(body) }),
  uploadResumeText: async (candidateId: string, resumeText: string) => {
    const form = new FormData();
    form.append('resume_text', resumeText);
    const res = await fetch(`${BASE_URL}/api/candidates/${candidateId}/upload-resume`, {
      method: 'POST',
      body: form,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || 'Resume upload failed');
    }
    return res.json();
  },
  uploadResumeFile: async (candidateId: string, file: ResumeUploadFile) => {
    const form = new FormData();
    form.append(
      'resume_file',
      {
        uri: file.uri,
        name: file.name,
        type: file.type ?? 'application/octet-stream',
      } as any
    );
    const res = await fetch(`${BASE_URL}/api/candidates/${candidateId}/upload-resume`, {
      method: 'POST',
      body: form,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || 'Resume upload failed');
    }
    return res.json();
  },
  startInterview: (body: { candidate_id: string; mode: string; round_type: string }) =>
    request<any>('/api/interviews/start', { method: 'POST', body: JSON.stringify(body) }),
  submitAnswer: (sessionId: string, answer: string) =>
    request<any>(`/api/interviews/${sessionId}/answer`, { method: 'POST', body: JSON.stringify({ answer }) }),
  getRanking: () => request<Ranking[]>('/api/recruiter/ranking'),
};
