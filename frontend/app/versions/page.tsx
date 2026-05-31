"use client"
import { useEffect, useState } from "react"
import { getResumeVersions, downloadPDF } from "../../lib/api"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card"
import { Button } from "../../components/ui/button"
import { Badge } from "../../components/ui/badge"

export default function VersionsPage() {
  const [versions, setVersions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchVersions()
  }, [])

  async function fetchVersions() {
    try {
      const data = await getResumeVersions()
      setVersions(data)
    } catch (error) {
      console.error("Failed to fetch versions:", error)
    } finally {
      setLoading(false)
    }
  }

  async function handleDownload(versionId: number) {
    try {
      const blob = await downloadPDF(versionId)
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `resume-${versionId}.pdf`
      a.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error("Failed to download:", error)
    }
  }

  return (
    <main className="min-h-screen px-5 py-6 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-5 py-4 backdrop-blur-xl">
          <Badge variant="outline">Resume Library</Badge>
          <h2 className="mt-3 font-display text-3xl text-white">Resume Versions</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
            View, compare, and download your tailored resume versions.
          </p>
        </header>

        {loading ? (
          <div className="text-center text-slate-400">Loading versions...</div>
        ) : versions.length === 0 ? (
          <Card className="bg-white/6">
            <CardContent className="py-8 text-center text-slate-400">
              No resume versions yet. Create one by applying to a job.
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {versions.map((v: any) => (
              <Card key={v.id} className="bg-white/6">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle>{v.version_name || `Version ${v.id}`}</CardTitle>
                      <CardDescription>{v.target_role}</CardDescription>
                    </div>
                    <Badge variant="secondary">{v.ats_score || "N/A"}</Badge>
                  </div>
                </CardHeader>
                <CardContent className="flex gap-2">
                  <Button size="sm" onClick={() => handleDownload(v.id)}>
                    Download PDF
                  </Button>
                  <Button size="sm" variant="outline">
                    View Details
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </main>
  )
}
