"use client"

import Link from "next/link"
import { useTheme } from "next-themes"

import { Badge } from "../components/ui/badge"
import { Button } from "../components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card"

const metrics = [
  { label: "Resumes tailored", value: "2.8k" },
  { label: "ATS uplift", value: "+34%" },
  { label: "Median time saved", value: "18 min" },
]

const features = [
  {
    title: "GitHub-aware matching",
    text: "Pulls the most relevant repos into each application so the resume reads like real work, not generic keywords.",
  },
  {
    title: "ATS-first scoring",
    text: "Highlights missing keywords, weak bullets, and formatting gaps before you export a PDF.",
  },
  {
    title: "LaTeX export",
    text: "Compiles a clean, single-page resume that is sharp enough for recruiters and parsers alike.",
  },
  {
    title: "Role-specific workflow",
    text: "Create a tailored version for each job without rebuilding your profile from scratch every time.",
  },
]

export default function Home() {
  const { theme, setTheme } = useTheme()

  return (
    <main className="relative min-h-screen overflow-hidden">
      <div className="hero-grid absolute inset-0 opacity-30" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.18),transparent_32%),radial-gradient(circle_at_right,rgba(59,130,246,0.1),transparent_28%)]" />

      <div className="relative mx-auto flex min-h-screen max-w-7xl flex-col px-5 py-6 sm:px-8 lg:px-10">
        <header className="flex flex-wrap items-center justify-between gap-4 rounded-[1.5rem] border border-white/10 bg-slate-950/50 px-5 py-4 backdrop-blur-xl">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-emerald-300">ResumeAgent</p>
            <h1 className="mt-1 font-display text-2xl text-white">AI resume optimization studio</h1>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <Button variant="ghost" size="sm" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>Toggle theme</Button>
            <Button href="/dashboard" variant="outline" size="sm">Dashboard</Button>
            <Button href="/apply" size="sm">Start a role</Button>
          </div>
        </header>

        <section className="grid flex-1 items-center gap-10 py-12 lg:grid-cols-[1.2fr_0.8fr] lg:py-16">
          <div className="space-y-8">
            <Badge variant="success">Live AI resume generation</Badge>
            <div className="max-w-3xl space-y-5">
              <h2 className="font-display text-5xl leading-[0.95] tracking-tight text-white sm:text-6xl lg:text-7xl">
                Turn your experience into a sharper, role-specific resume.
              </h2>
              <p className="max-w-2xl text-lg leading-8 text-slate-300 sm:text-xl">
                ResumeAgent analyzes a job description, ranks your GitHub projects, rewrites bullets, and exports a polished PDF without the usual template churn.
              </p>
            </div>

            <div className="flex flex-wrap gap-3">
              <Button href="/apply" size="lg">Build a tailored resume</Button>
              <Button href="/dashboard" variant="outline" size="lg">View dashboard</Button>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              {metrics.map((metric) => (
                <Card key={metric.label} className="bg-white/6">
                  <CardContent className="px-5 py-5">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-400">{metric.label}</p>
                    <p className="mt-3 font-display text-3xl text-white">{metric.value}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          <Card className="bg-slate-950/80 text-white">
            <CardHeader>
              <Badge variant="default">Pipeline preview</Badge>
              <CardTitle className="mt-4 text-2xl">From JD to PDF in one flow</CardTitle>
              <CardDescription>
                A focused dashboard for uploads, matching, scoring, and export.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {[
                ["1. Ingest", "Resume, JD, and repo links."],
                ["2. Rank", "Projects are scored by relevance."],
                ["3. Optimize", "Bullets are rewritten for impact."],
                ["4. Export", "Single-page PDF is compiled."],
              ].map(([step, detail]) => (
                <div key={step} className="flex items-start gap-4 rounded-2xl border border-white/10 bg-white/5 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-400/15 text-sm font-semibold text-emerald-300">{step.split(".")[0]}</div>
                  <div>
                    <p className="font-medium text-white">{step}</p>
                    <p className="text-sm text-slate-300">{detail}</p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </section>

        <section className="grid gap-5 pb-8 lg:grid-cols-2">
          {features.map((feature) => (
            <Card key={feature.title} className="bg-white/7">
              <CardHeader>
                <CardTitle>{feature.title}</CardTitle>
                <CardDescription>{feature.text}</CardDescription>
              </CardHeader>
            </Card>
          ))}
        </section>
      </div>
    </main>
  )
}
