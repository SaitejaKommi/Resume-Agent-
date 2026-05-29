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
