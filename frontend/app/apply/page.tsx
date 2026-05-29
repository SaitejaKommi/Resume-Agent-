"use client"
import { useState, useEffect } from "react"
import { Button } from "../../components/ui/button"
import ResumeUploader from "../../components/ResumeUploader"
import { uploadJD, createApplication, getApplication } from "../../lib/api"
import AtsScore from "../../components/AtsScore"

export default function ApplyPage() {
  const [step, setStep] = useState(1)
  const [resumeId, setResumeId] = useState<number | null>(null)
  const [reposText, setReposText] = useState("")
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
    const app = await createApplication({ resume_id: resumeId, job_id: job.id, github_repos: reposText.split(/\r?\n/).filter(Boolean) })
    setApplicationId(app.id)
    setStep(3)
    setProcessing(true)
  }

  useEffect(() => {
    let t: number | undefined
    if (step === 3 && applicationId) {
      t = window.setInterval(async () => {
        const a = await getApplication(applicationId)
        if (a && a.ats_score !== undefined) {
          setResult(a)
          setProcessing(false)
          setStep(4)
          if (t) clearInterval(t)
        }
      }, 2000)
    }
    return () => { if (t) clearInterval(t) }
  }, [step, applicationId])

  return (
    <main className="p-6">
      <h2 className="text-2xl font-bold">New Application</h2>
      <div className="mt-6">
        {step === 1 && (
          <section>
            <h3 className="font-semibold">Step 1 — Upload Resume</h3>
            <ResumeUploader onDone={onUploadDone} />
            <div className="mt-4">
              <label className="block text-sm">GitHub repo URLs (one per line)</label>
              <textarea value={reposText} onChange={(e) => setReposText(e.target.value)} className="mt-1 w-full p-2 border rounded" rows={4} />
            </div>
            <div className="mt-4">
              <Button onClick={() => setStep(1)} disabled>Next</Button>
            </div>
          </section>
        )}

        {step === 2 && (
          <section>
            <h3 className="font-semibold">Step 2 — Job Description</h3>
            <textarea value={jdText} onChange={(e) => setJdText(e.target.value)} className="mt-1 w-full p-2 border rounded" rows={8} />
            <div className="mt-4 flex gap-2">
              <Button onClick={() => setStep(1)} variant="ghost">Back</Button>
              <Button onClick={submitJob} disabled={!jdText}>Process with AI</Button>
            </div>
          </section>
        )}

        {step === 3 && (
          <section>
            <h3 className="font-semibold">Step 3 — Processing</h3>
            <div className="mt-4">
              <ol className="list-decimal ml-6 space-y-2">
                <li>Analyzing JD...</li>
                <li>Reading GitHub repos...</li>
                <li>Ranking projects...</li>
                <li>Optimizing bullets...</li>
                <li>Generating PDF...</li>
              </ol>
              <div className="mt-4">{processing ? 'Processing...' : 'Waiting...'}</div>
            </div>
          </section>
        )}

        {step === 4 && result && (
          <section>
            <h3 className="font-semibold">Step 4 — Results</h3>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              <AtsScore score={result.ats_score ?? 0} missingKeywords={result.missing_keywords ?? []} suggestions={result.suggestions ?? []} />
              <div>
                <h4 className="font-medium">Projects</h4>
                <ul className="mt-2 list-disc ml-6">
                  {(result.projects || []).map((p: any, i: number) => <li key={i}>{p.name} — relevance {p.relevance_score}</li>)}
                </ul>
                <div className="mt-4">
                  <a className="inline-block" href={`/download/${applicationId}`}><Button>Download PDF</Button></a>
                  <Button variant="ghost" className="ml-2" onClick={() => { setStep(1); setResult(null); }}>Try another role</Button>
                </div>
              </div>
            </div>
          </section>
        )}
      </div>
    </main>
  )
}
