import axios from "axios"

const client = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000", withCredentials: true })

export async function uploadResume(file: File): Promise<{ resume_id: number }> {
  const fd = new FormData()
  fd.append("file", file)
  const res = await client.post("/resume/upload", fd, { headers: { "Content-Type": "multipart/form-data" } })
  return res.data
}

export async function uploadJD(jdText: string): Promise<{ id: number }> {
  const res = await client.post("/job/upload", { jd_text: jdText })
  return res.data
}

export async function createApplication(payload: { resume_id: number; job_id: number; github_repos: string[] }) {
  const res = await client.post("/application/create", payload)
  return res.data
}

export async function getProfile() {
  const res = await client.get("/profile/me")
  return res.data
}

export async function updateProfile(payload: {
  headline?: string | null
  summary?: string | null
  education_json?: any[] | null
  experience_json?: any[] | null
  skills_json?: any[] | null
  certifications_json?: any[] | null
  achievements_json?: any[] | null
  projects_json?: any[] | null
  github_json?: Record<string, any> | null
  portfolio_links_json?: any[] | null
}) {
  const res = await client.patch("/profile/me", payload)
  return res.data
}

export async function getResumeVersions() {
  const res = await client.get("/resume-versions/list")
  return res.data?.items || []
}

export async function getApplication(id: number) {
  const res = await client.get(`/application/${id}`)
  return res.data
}

export async function getApplications() {
  const res = await client.get("/application/list")
  return res.data?.items || []
}

export async function downloadPDF(applicationId: number) {
  const res = await client.get(`/download/${applicationId}`, { responseType: 'blob' })
  return res.data
}
