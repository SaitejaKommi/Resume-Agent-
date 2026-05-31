"use client"

import { useEffect, useState } from "react"

import { Badge } from "../../components/ui/badge"
import { Button } from "../../components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card"
import { getProfile, updateProfile } from "../../lib/api"

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null)
  const [headline, setHeadline] = useState("")
  const [summary, setSummary] = useState("")
  const [skills, setSkills] = useState("")
  const [projects, setProjects] = useState("")
  const [portfolioLinks, setPortfolioLinks] = useState("")
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    getProfile().then((res) => {
      setProfile(res)
      setHeadline(res?.headline || "")
      setSummary(res?.summary || "")
      setSkills((res?.skills_json || []).join(", "))
      setProjects((res?.projects_json || []).map((item: any) => (typeof item === "string" ? item : item.name || JSON.stringify(item))).join("\n"))
      setPortfolioLinks((res?.portfolio_links_json || []).join(", "))
    }).catch(() => setProfile(null))
  }, [])

  async function onSave() {
    setSaving(true)
    try {
      const updated = await updateProfile({
        headline,
        summary,
        skills_json: skills.split(",").map((item) => item.trim()).filter(Boolean),
        projects_json: projects.split("\n").map((item) => item.trim()).filter(Boolean).map((name) => ({ name })),
        portfolio_links_json: portfolioLinks.split(",").map((item) => item.trim()).filter(Boolean),
      })
      setProfile(updated)
    } finally {
      setSaving(false)
    }
  }

  return (
    <main className="min-h-screen px-5 py-6 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-5xl space-y-6">
        <header className="rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-5 py-4 backdrop-blur-xl">
          <Badge variant="success">Master profile</Badge>
          <h2 className="mt-3 font-display text-3xl text-white">Edit your source of truth</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
            This profile powers every future resume generation, so update it once and reuse it everywhere.
          </p>
        </header>

        <Card className="bg-white/6">
          <CardHeader>
            <CardTitle>Profile completeness</CardTitle>
            <CardDescription>Resume uploads and GitHub syncs feed this score automatically.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-4xl font-display text-white">{profile?.profile_completeness ?? 0}%</p>
                <p className="mt-2 text-sm text-slate-300">{profile?.source_resume_id ? "Seeded from your latest resume upload." : "Create your first profile by uploading a resume."}</p>
              </div>
              <div className="h-3 w-full max-w-xs overflow-hidden rounded-full bg-white/10">
                <div className="h-full rounded-full bg-emerald-400" style={{ width: `${profile?.profile_completeness ?? 0}%` }} />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-white/6">
          <CardHeader>
            <CardTitle>Profile fields</CardTitle>
            <CardDescription>Keep the fields you want to reuse across every application up to date.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="mb-2 block text-sm text-slate-300">Headline</label>
              <input value={headline} onChange={(e) => setHeadline(e.target.value)} className="w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-emerald-400" placeholder="Full-Stack Engineer focused on AI products" />
            </div>
            <div>
              <label className="mb-2 block text-sm text-slate-300">Summary</label>
              <textarea value={summary} onChange={(e) => setSummary(e.target.value)} className="min-h-[140px] w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-emerald-400" />
            </div>
            <div>
              <label className="mb-2 block text-sm text-slate-300">Skills, comma separated</label>
              <textarea value={skills} onChange={(e) => setSkills(e.target.value)} className="min-h-[110px] w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-emerald-400" />
            </div>
            <div>
              <label className="mb-2 block text-sm text-slate-300">Projects, one per line</label>
              <textarea value={projects} onChange={(e) => setProjects(e.target.value)} className="min-h-[140px] w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-emerald-400" />
            </div>
            <div>
              <label className="mb-2 block text-sm text-slate-300">Portfolio links, comma separated</label>
              <input value={portfolioLinks} onChange={(e) => setPortfolioLinks(e.target.value)} className="w-full rounded-2xl border border-white/12 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-emerald-400" placeholder="https://yourportfolio.com, https://github.com/you" />
            </div>
            <div className="flex justify-end">
              <Button onClick={onSave} disabled={saving}>{saving ? "Saving..." : "Save profile"}</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}