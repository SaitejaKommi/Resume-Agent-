"use client"
import { useEffect, useState } from "react"
import { getApplications } from "../../lib/api"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card"
import { Badge } from "../../components/ui/badge"

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [columns, setColumns] = useState<Record<string, any[]>>({})

  const statusColumns = ["saved", "applied", "online_assessment", "interview", "final_round", "offer", "rejected"]

  useEffect(() => {
    fetchApplications()
  }, [])

  async function fetchApplications() {
    try {
      const data = await getApplications()
      setApplications(data)
      // Organize by kanban status
      const grouped: Record<string, any[]> = {}
      statusColumns.forEach(col => {
        grouped[col] = data.filter((a: any) => (a.kanban_status || "saved") === col)
      })
      setColumns(grouped)
    } catch (error) {
      console.error("Failed to fetch applications:", error)
    } finally {
      setLoading(false)
    }
  }

  const columnLabels: Record<string, string> = {
    saved: "Saved",
    applied: "Applied",
    online_assessment: "Online Assessment",
    interview: "Interview",
    final_round: "Final Round",
    offer: "Offer",
    rejected: "Rejected",
  }

  const statusBadgeVariants: Record<string, any> = {
    saved: "outline",
    applied: "secondary",
    online_assessment: "default",
    interview: "default",
    final_round: "default",
    offer: "secondary",
    rejected: "destructive",
  }

  return (
    <main className="min-h-screen px-5 py-6 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-full space-y-6">
        <header className="rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-5 py-4 backdrop-blur-xl">
          <Badge variant="outline">Job Pipeline</Badge>
          <h2 className="mt-3 font-display text-3xl text-white">Applications</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
            Track your job applications through the pipeline.
          </p>
        </header>

        {loading ? (
          <div className="text-center text-slate-400">Loading applications...</div>
        ) : (
          <div className="grid auto-cols-max gap-4 overflow-x-auto pb-4">
            {statusColumns.map((col) => (
              <div key={col} className="min-w-[300px]">
                <div className="mb-3 flex items-center justify-between rounded-lg bg-white/5 px-3 py-2">
                  <h3 className="font-semibold text-white">{columnLabels[col]}</h3>
                  <Badge variant="secondary">{(columns[col] || []).length}</Badge>
                </div>
                <div className="space-y-3">
                  {(columns[col] || []).map((app: any) => (
                    <Card key={app.id} className="bg-white/6 cursor-pointer hover:bg-white/8 transition">
                      <CardContent className="pt-4">
                        <p className="font-semibold text-white text-sm line-clamp-1">{app.company || "Unknown Company"}</p>
                        <p className="text-xs text-slate-400 line-clamp-1">{app.role_title || "Position"}</p>
                        {app.ats_score && (
                          <div className="mt-2 text-xs">
                            <span className="text-emerald-400 font-bold">ATS: {app.ats_score}</span>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                  {(columns[col] || []).length === 0 && (
                    <div className="rounded-lg border border-white/10 bg-white/5 px-3 py-6 text-center text-xs text-slate-500">
                      No applications
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  )
}
