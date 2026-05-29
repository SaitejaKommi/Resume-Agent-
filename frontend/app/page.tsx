"use client"
import Link from "next/link"
import { useTheme } from "next-themes"
import { Button } from "../components/ui/button"

export default function Home() {
  const { theme, setTheme } = useTheme()
  return (
    <main className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <div className="container mx-auto px-4 py-16">
        <header className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">ResumeAgent</h1>
          <div className="flex items-center gap-2">
            <Button variant="ghost" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
              Toggle
            </Button>
            <Link href="/dashboard"><Button>Dashboard</Button></Link>
          </div>
        </header>

        <section className="mt-12 text-center">
          <h2 className="text-4xl font-extrabold">AI Resume Copilot for Developers</h2>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Generate role-specific, ATS-optimized resumes using your GitHub projects automatically.</p>
          <div className="mt-6">
            <Link href="/dashboard"><Button size="lg">Get Started — Dashboard</Button></Link>
          </div>
        </section>

        <section className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { title: 'GitHub-aware', text: 'Automatically surface relevant projects.' },
            { title: 'ATS Optimized', text: 'Keyword-aware resume improvements.' },
            { title: 'LaTeX Quality', text: 'High-fidelity single-page PDF output.' },
            { title: 'Role-Specific', text: 'Tailor resumes per role automatically.' },
          ].map((f) => (
            <div key={f.title} className="p-6 bg-gray-50 dark:bg-gray-800 rounded-lg shadow">
              <h3 className="font-semibold">{f.title}</h3>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">{f.text}</p>
            </div>
          ))}
        </section>
      </div>
    </main>
  )
}
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ResumeWorkbench } from "@/components/resume-workbench";

export default function Page() {
  return (
    <main className="min-h-screen">
      <section className="hero-grid border-b border-slate-200/70">
        <div className="mx-auto max-w-7xl px-6 py-8 lg:px-10">
          <div className="flex items-center justify-between rounded-full border border-slate-200 bg-white/80 px-5 py-3 shadow-sm backdrop-blur">
            <div>
              <p className="font-display text-lg font-semibold tracking-tight text-slate-950">ResumeAgent</p>
            </div>
            <Button href="http://localhost:8000/auth/github/login" size="sm" className="hidden md:inline-flex">
              Sign in with GitHub
            </Button>
          </div>
        </div>

        <div className="mx-auto grid max-w-7xl gap-14 px-6 pb-16 pt-8 lg:grid-cols-[1.05fr_0.95fr] lg:px-10 lg:pb-24 lg:pt-14">
          <div className="space-y-8">
            <div className="inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700">
              AI resume optimization for modern hiring loops
            </div>
            <div className="space-y-5">
              <h1 className="max-w-3xl font-display text-5xl font-semibold tracking-tight text-slate-950 md:text-7xl">
                Turn every resume into a sharper, more relevant application.
              </h1>
              <p className="max-w-2xl text-lg leading-8 text-slate-600 md:text-xl">
                ResumeAgent combines PDF ingestion, job-description extraction, ATS scoring, and GitHub OAuth so candidates can tailor faster and apply with confidence.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Button href="http://localhost:8000/auth/github/login" size="lg">
                Connect GitHub
              </Button>
              <Button href="http://localhost:8000/health" variant="outline" size="lg">
                View backend health
              </Button>
            </div>
            <div className="grid gap-4 sm:grid-cols-3">
              {[
                ["Resume parsing", "Structured JSON output for downstream workflows."],
                ["Skill matching", "Compare resumes against target roles instantly."],
                ["Secure storage", "Persist GitHub tokens and candidate data in PostgreSQL."],
              ].map(([title, description]) => (
                <Card key={title} className="border-slate-200/80 bg-white/85">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">{title}</CardTitle>
                    <CardDescription>{description}</CardDescription>
                  </CardHeader>
                </Card>
              ))}
            </div>
          </div>

          <div className="rounded-[2rem] border border-slate-200/80 bg-white/70 p-4 shadow-glow backdrop-blur">
            <ResumeWorkbench />
          </div>
        </div>
      </section>
      <section className="mx-auto max-w-7xl px-6 py-12 lg:px-10">
        <div className="grid gap-6 md:grid-cols-3">
          {[
            ["FastAPI backend", "Clear route/service separation and SQLAlchemy models."],
            ["Tailwind + shadcn", "Custom UI primitives with an elevated visual system."],
            ["Docker-ready", "Frontend, backend, and PostgreSQL can run from one compose file."],
          ].map(([title, description]) => (
            <Card key={title}>
              <CardHeader>
                <CardTitle>{title}</CardTitle>
                <CardDescription>{description}</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-6 text-slate-600">
                  Built to be extended with LLM extraction, scoring, and application automation.
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>
    </main>
  );
}
