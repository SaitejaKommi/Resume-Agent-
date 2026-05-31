"use client"
import { useState, useEffect } from "react"
import { Button } from "../../components/ui/button"
import ResumeUploader from "../../components/ResumeUploader"
import { uploadJD, createApplication, getApplication } from "../../lib/api"
import AtsScore from "../../components/AtsScore"
import { Badge } from "../../components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card"

export default function ApplyPage() {
  const [step, setStep] = useState(1)
  const [resumeId, setResumeId] = useState<number | null>(null)
  const [reposText, setReposText] = useState("")
  const [company, setCompany] = useState("")
  const [roleTitle, setRoleTitle] = useState("")
  const [status, setStatus] = useState("saved")
  const [jdText, setJdText] = useState("")
  const [applicationId, setApplicationId] = useState<number | null>(null)
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState<any>(null)

  async function onUploadDone(resume_id: number) {
    setResumeId(resume_id)
    setStep(2)
  }

  async function submitJob() {
    if (!resumeId) return
    const job = await uploadJD(jdText)
    const app = await createApplication({
      resume_id: resumeId,
      job_id: job.id,
      github_repos: reposText.split(/\r?\n/).filter(Boolean),
      company,
      role_title: roleTitle,
      status,
      date_applied: status === "applied" ? new Date().toISOString() : null,
    })
    setApplicationId(app.id)
    setStep(3)
    setProcessing(true)
  }

  useEffect(() => {
    let t: number | undefined
    if (step === 3 && applicationId) {
      t = window.setInterval(async () => {
        try {
          const a = await getApplication(applicationId)
          if (a && a.ats_score !== undefined) {
            setResult(a)
            setProcessing(false)
            setStep(4)
            if (t) clearInterval(t)
          }
        } catch {
          // Keep polling while the backend is warming up or temporarily offline.
        }
      }, 2000)
    }
    return () => { if (t) clearInterval(t) }
  }, [step, applicationId])

  return (
    <main className="min-h-screen px-5 py-6 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-5 py-4 backdrop-blur-xl">
          <Badge variant="success">4-step workflow</Badge>
          <h2 className="mt-3 font-display text-3xl text-white">New application</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
            Upload your baseline resume, add the job description and repo links, then let the pipeline produce a tailored export.
          </p>
        </header>

        <div className="grid gap-6 lg:grid-cols-[0.32fr_0.68fr]">
          <Card className="h-fit bg-white/6">
            <CardHeader>
              <CardTitle>Progress</CardTitle>
              <CardDescription>Track the workflow from upload to export.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {[
                [1, "Upload resume", step >= 1],
                [2, "Add JD and repos", step >= 2],
                [3, "Process with AI", step >= 3],
                [4, "Review results", step >= 4],
              ].map(([index, label, done]) => (
                <div key={label} className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
                  <div className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-semibold ${done ? "bg-emerald-400/20 text-emerald-300" : "bg-white/10 text-slate-300"}`}>{index}</div>
                  <span className="text-sm text-white">{label}</span>
                </div>
              ))}
            </CardContent>
          </Card>

          <div className="space-y-6">
        {step === 1 && (
          <Card className="bg-white/6">
            <CardHeader>
              <CardTitle>Step 1 — Upload resume</CardTitle>
              <CardDescription>Start with the base resume you want the system to tailor.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-5">
            <ResumeUploader onDone={onUploadDone} />
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm text-slate-300">Company</label>
                  <input value={company} onChange={(e) => setCompany(e.target.value)} className="w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-400 focus:border-emerald-400" placeholder="Google, Stripe, OpenAI..." />
                </div>
                <div>
                  <label className="mb-2 block text-sm text-slate-300">Role title</label>
                  <input value={roleTitle} onChange={(e) => setRoleTitle(e.target.value)} className="w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-400 focus:border-emerald-400" placeholder="Frontend Engineer" />
                </div>
              </div>
              <div>
                <label className="mb-2 block text-sm text-slate-300">Application status</label>
                <select value={status} onChange={(e) => setStatus(e.target.value)} className="w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-emerald-400">
                  <option value="saved">Saved</option>
                  <option value="applied">Applied</option>
                  <option value="oa">OA</option>
                  <option value="interview">Interview</option>
                  <option value="final_round">Final Round</option>
                  <option value="offer">Offer</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
              <div>
                <label className="mb-2 block text-sm text-slate-300">GitHub repo URLs</label>
                <textarea value={reposText} onChange={(e) => setReposText(e.target.value)} className="min-h-[160px] w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-400 focus:border-emerald-400" placeholder="One repo per line" rows={4} />
              </div>
              <div className="flex justify-end">
                <Button onClick={() => setStep(2)} variant="secondary" disabled={!resumeId}>
                  Continue
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {step === 2 && (
          <Card className="bg-white/6">
            <CardHeader>
              <CardTitle>Step 2 — Add job description</CardTitle>
              <CardDescription>Paste the role description and optional notes before processing.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-5">
              <textarea value={jdText} onChange={(e) => setJdText(e.target.value)} className="min-h-[240px] w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-400 focus:border-emerald-400" placeholder="Paste the job description here" rows={8} />
              <div className="flex flex-wrap gap-3">
                <Button onClick={() => setStep(1)} variant="ghost">Back</Button>
                <Button onClick={submitJob} disabled={!jdText}>Process with AI</Button>
              </div>
            </CardContent>
          </Card>
        )}

        {step === 3 && (
          <Card className="bg-white/6">
            <CardHeader>
              <CardTitle>Step 3 — Processing</CardTitle>
              <CardDescription>The backend is parsing, ranking, and generating the tailored resume.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-3 md:grid-cols-2">
                {[
                  "Analyzing the job description",
                  "Reading GitHub repositories",
                  "Ranking projects by relevance",
                  "Optimizing resume bullets",
                  "Generating the final PDF",
                ].map((item, index) => (
                  <div key={item} className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
                    <span className="flex h-8 w-8 items-center justify-center rounded-full bg-white/10 text-sm text-white">{index + 1}</span>
                    <span className="text-sm text-slate-200">{item}</span>
                  </div>
                ))}
              </div>
              <div className="mt-5 text-sm text-slate-300">{processing ? "Processing your application..." : "Waiting for the pipeline to complete."}</div>
            </CardContent>
          </Card>
        )}

        {step === 4 && result && (
          <Card className="bg-white/6">
            <CardHeader>
              <CardTitle>Step 4 — Results</CardTitle>
              <CardDescription>Review score, recommendations, and ranked projects before downloading.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-5 xl:grid-cols-[0.9fr_1.1fr]">
                <AtsScore score={result.ats_score ?? 0} missingKeywords={result.missing_keywords ?? []} suggestions={result.suggestions ?? []} />
                <div className="space-y-5 rounded-[1.5rem] border border-white/10 bg-white/5 p-5">
                  <div>
                    <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Projects ranked</p>
                    <div className="mt-4 space-y-3">
                      {(result.projects || []).map((p: any, i: number) => (
                        <div key={i} className="rounded-2xl border border-white/10 bg-slate-950/40 px-4 py-3">
                          <div className="flex items-center justify-between gap-3">
                            <span className="font-medium text-white">{p.name}</span>
                            <Badge variant="success">{p.relevance_score}</Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-3">
                    <a className="inline-flex" href={`/download/${applicationId}`}>
                      <Button>Download PDF</Button>
                    </a>
                    <Button variant="ghost" onClick={() => { setStep(1); setResult(null); }}>Try another role</Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
          </div>
        </div>
      </div>
    </main>
  )
}
