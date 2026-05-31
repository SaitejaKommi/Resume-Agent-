"use client"
import { useEffect, useState } from "react"
import Link from "next/link"
import { Button } from "../../components/ui/button"
import { Badge } from "../../components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card"
import { getApplications, getProfile, getResumeVersions } from "../../lib/api"
import AtsScore from "../../components/AtsScore"

type Application = {
  id: number
  company: string | null
  role_title: string | null
  job_title: string
  ats_score: number
  status: string
  created_at: string
}

type ResumeVersion = {
  id: number
  version_name: string
  target_role: string | null
  ats_score: number
  created_at: string
}

export default function Dashboard() {
  const [apps, setApps] = useState<Application[]>([])
  const [versions, setVersions] = useState<ResumeVersion[]>([])
  const [profile, setProfile] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getApplications(), getResumeVersions(), getProfile()])
      .then(([applications, resumeVersions, masterProfile]) => {
        setApps(applications || [])
        setVersions(resumeVersions || [])
        setProfile(masterProfile)
      })
      .catch(() => {
        setApps([])
        setVersions([])
        setProfile(null)
      })
      .finally(() => setLoading(false))
  }, [])

  const avg = apps.length ? Math.round(apps.reduce((s, a) => s + a.ats_score, 0) / apps.length) : 0
  const profileCompleteness = profile?.profile_completeness ?? 0

  return (
    <main className="min-h-screen px-5 py-6 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="flex flex-wrap items-center justify-between gap-4 rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-5 py-4 backdrop-blur-xl">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-emerald-300">ResumeAgent</p>
            <h2 className="mt-1 font-display text-3xl text-white">Dashboard</h2>
            <p className="text-sm text-slate-300">Track application quality, export status, and recent resume generations.</p>
          </div>
          <div className="flex gap-2">
            <Link href="/apply"><Button>+ New application</Button></Link>
            <Button variant="outline">Upload resume</Button>
          </div>
        </header>

        <div className="grid gap-5 lg:grid-cols-4">
          {[
            ["Applications", `${apps.length}`],
            ["Average ATS", `${avg}%`],
            ["Resume versions", `${versions.length}`],
            ["Active opportunities", loading ? "..." : apps.filter((a) => ["saved", "applied", "oa", "interview", "final_round"].includes(a.status)).length],
          ].map(([label, value]) => (
            <Card key={label} className="bg-white/6">
              <CardContent className="px-5 py-5">
                <p className="text-xs uppercase tracking-[0.24em] text-slate-400">{label}</p>
                <p className="mt-3 font-display text-3xl text-white">{value}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
          <Card className="bg-white/6">
            <CardHeader>
              <CardTitle>Application pipeline</CardTitle>
              <CardDescription>Track where each role sits in your job search.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-hidden rounded-[1.25rem] border border-white/10">
                <table className="min-w-full divide-y divide-white/10 text-left">
                  <thead className="bg-white/5 text-xs uppercase tracking-[0.24em] text-slate-400">
                    <tr>
                      <th className="px-4 py-3">Role</th>
                      <th className="px-4 py-3">ATS score</th>
                      <th className="px-4 py-3">Status</th>
                      <th className="px-4 py-3">Date</th>
                      <th className="px-4 py-3">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/8">
                    {loading ? (
                      <tr>
                        <td colSpan={5} className="px-4 py-10 text-center text-slate-300">Loading your applications...</td>
                      </tr>
                    ) : apps.length ? (
                      apps.map((a) => (
                        <tr key={a.id} className="bg-white/[0.03]">
                          <td className="px-4 py-4 font-medium text-white">
                            <div>{a.role_title || a.job_title}</div>
                            <div className="text-xs text-slate-400">{a.company || "Unspecified company"}</div>
                          </td>
                          <td className="px-4 py-4">
                            <Badge variant={a.ats_score > 75 ? "success" : a.ats_score > 50 ? "warning" : "destructive"}>{a.ats_score}</Badge>
                          </td>
                          <td className="px-4 py-4 text-slate-300">{a.status}</td>
                          <td className="px-4 py-4 text-slate-300">{new Date(a.created_at).toLocaleDateString()}</td>
                          <td className="px-4 py-4">
                            <Button href={`/download/${a.id}`} size="sm" variant="outline">Download</Button>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={5} className="px-4 py-10 text-center text-slate-300">No applications yet. Start a role to generate your first tailored resume.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-950/80 text-white">
            <CardHeader>
              <Badge variant="default">Workspace health</Badge>
              <CardTitle className="mt-4">Master profile completeness</CardTitle>
              <CardDescription>The source of truth that powers every future generation.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-5">
              <div className="rounded-[1.5rem] border border-white/10 bg-white/5 p-5">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Profile completeness</p>
                    <p className="mt-2 font-display text-4xl text-white">{profileCompleteness}%</p>
                  </div>
                  <Button href="/profile" variant="outline" size="sm">Edit profile</Button>
                </div>
                <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/10">
                  <div className="h-full rounded-full bg-emerald-400" style={{ width: `${profileCompleteness}%` }} />
                </div>
              </div>
              <AtsScore score={avg} missingKeywords={[]} suggestions={[
                "Add sharper verbs to low-impact bullets.",
                "Mirror role-specific keywords from the JD.",
                "Keep the export to a single page where possible.",
              ]} />
              <div className="grid gap-3">
                {[
                  ["Analysis", "JD parsing and keyword mapping"],
                  ["Ranking", "GitHub projects scored by relevance"],
                  ["Generation", "LaTeX PDF compiled successfully"],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">{label}</p>
                    <p className="mt-1 text-sm text-slate-100">{value}</p>
                  </div>
                ))}
              </div>

              <div className="rounded-[1.5rem] border border-white/10 bg-white/5 p-5">
                <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Recent versions</p>
                <div className="mt-4 space-y-3">
                  {versions.slice(0, 3).map((version) => (
                    <div key={version.id} className="rounded-2xl border border-white/10 bg-slate-950/40 px-4 py-3">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <p className="font-medium text-white">{version.version_name}</p>
                          <p className="text-xs text-slate-400">{version.target_role || "General"}</p>
                        </div>
                        <Badge variant="success">{version.ats_score}</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  )
}
