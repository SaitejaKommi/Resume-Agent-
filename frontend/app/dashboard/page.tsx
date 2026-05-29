"use client"
import { useEffect, useState } from "react"
import Link from "next/link"
import { Button } from "../../components/ui/button"
import { Badge } from "../../components/ui/badge"
import { getApplications } from "../../lib/api"
import AtsScore from "../../components/AtsScore"

type Application = {
  id: number
  job_title: string
  ats_score: number
  status: string
  created_at: string
}

export default function Dashboard() {
  const [apps, setApps] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getApplications().then((res) => {
      setApps(res || [])
    }).finally(() => setLoading(false))
  }, [])

  const avg = apps.length ? Math.round(apps.reduce((s, a) => s + a.ats_score, 0) / apps.length) : 0

  return (
    <main className="p-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <div className="flex gap-2">
          <Link href="/apply"><Button>+ New Application</Button></Link>
          <Button variant="outline">Upload Resume</Button>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
          <div className="text-sm text-gray-500">Resumes uploaded</div>
          <div className="text-xl font-semibold">{/* placeholder */} 3</div>
        </div>
        <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
          <div className="text-sm text-gray-500">Applications</div>
          <div className="text-xl font-semibold">{apps.length}</div>
        </div>
        <div className="p-4 bg-white dark:bg-gray-800 rounded shadow flex items-center gap-4">
          <div>
            <div className="text-sm text-gray-500">Avg ATS Score</div>
            <div className="text-xl font-semibold">{avg}</div>
          </div>
          <AtsScore score={avg} missingKeywords={[]} suggestions={[]} />
        </div>
      </div>

      <section className="mt-8">
        <h3 className="font-semibold mb-2">Recent Applications</h3>
        <div className="overflow-auto bg-white dark:bg-gray-800 rounded shadow">
          <table className="min-w-full divide-y">
            <thead className="bg-gray-50 dark:bg-gray-900">
              <tr>
                <th className="px-4 py-2 text-left">Job Title</th>
                <th className="px-4 py-2">ATS Score</th>
                <th className="px-4 py-2">Status</th>
                <th className="px-4 py-2">Date</th>
                <th className="px-4 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? <tr><td colSpan={5} className="p-4">Loading...</td></tr> : (
                apps.map((a) => (
                  <tr key={a.id} className="border-t">
                    <td className="px-4 py-2">{a.job_title}</td>
                    <td className="px-4 py-2"><Badge variant={a.ats_score>75?"success":a.ats_score>50?"warning":"destructive"}>{a.ats_score}</Badge></td>
                    <td className="px-4 py-2">{a.status}</td>
                    <td className="px-4 py-2">{new Date(a.created_at).toLocaleDateString()}</td>
                    <td className="px-4 py-2"><Button size="sm">Download</Button></td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  )
}
