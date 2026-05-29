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
