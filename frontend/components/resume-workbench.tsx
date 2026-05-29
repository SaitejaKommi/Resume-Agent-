"use client";

import { useEffect, useState } from "react";

import axios from "axios";
import { useDropzone } from "react-dropzone";
import { Worker, Viewer } from "@react-pdf-viewer/core";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

type Metrics = {
  health: string;
  uploads: number;
  atsScore: number;
};

const defaultMetrics: Metrics = {
  health: "checking...",
  uploads: 0,
  atsScore: 86,
};

export function ResumeWorkbench() {
  const [metrics, setMetrics] = useState(defaultMetrics);
  const [jobDescription, setJobDescription] = useState(
    "Senior Full-Stack Engineer with React, FastAPI, PostgreSQL, and AI workflow experience.",
  );
  const [fileUrl, setFileUrl] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>("No file selected");

  useEffect(() => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    axios
      .get(`${apiBase}/health`)
      .then(() => setMetrics((current) => ({ ...current, health: "online" })))
      .catch(() => setMetrics((current) => ({ ...current, health: "offline" })));
  }, []);

  useEffect(() => {
    return () => {
      if (fileUrl) {
        URL.revokeObjectURL(fileUrl);
      }
    };
  }, [fileUrl]);

  const onDrop = (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    setFileUrl(url);
    setFileName(file.name);
    setMetrics((current) => ({ ...current, uploads: current.uploads + 1 }));
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    multiple: false,
  });

  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
      <Card className="overflow-hidden border-slate-200/80 bg-white/80">
        <CardHeader>
          <CardTitle>Resume intelligence workspace</CardTitle>
          <CardDescription>Drop a PDF, paste a job description, and inspect the AI-ready pipeline.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div
            {...getRootProps()}
            className={`cursor-pointer rounded-3xl border border-dashed p-8 transition ${isDragActive ? "border-emerald-500 bg-emerald-50" : "border-slate-300 bg-slate-50/70"}`}
          >
            <input {...getInputProps()} />
            <div className="space-y-2 text-center">
              <p className="text-lg font-semibold text-slate-950">{isDragActive ? "Drop the resume PDF" : "Drag and drop a resume PDF"}</p>
              <p className="text-sm text-slate-500">Uploaded file: {fileName}</p>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Backend</p>
              <p className="mt-2 text-2xl font-semibold text-slate-950">{metrics.health}</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Uploads</p>
              <p className="mt-2 text-2xl font-semibold text-slate-950">{metrics.uploads}</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">ATS score</p>
              <p className="mt-2 text-2xl font-semibold text-slate-950">{metrics.atsScore}%</p>
            </div>
          </div>

          <div className="space-y-3">
            <label className="text-sm font-medium text-slate-700">Job description</label>
            <Textarea value={jobDescription} onChange={(event) => setJobDescription(event.target.value)} />
          </div>

          <div className="flex flex-wrap gap-3">
            <Button>Generate ATS Analysis</Button>
            <Button variant="outline">Export tailored resume</Button>
          </div>
        </CardContent>
      </Card>

      <Card className="overflow-hidden border-slate-200/80 bg-slate-950 text-white shadow-glow">
        <CardHeader>
          <CardTitle className="text-white">Preview</CardTitle>
          <CardDescription className="text-slate-300">The viewer renders uploaded PDFs without leaving the workspace.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="min-h-[540px] overflow-hidden rounded-3xl bg-white p-4 text-slate-950">
            {fileUrl ? (
              <Worker workerUrl="https://unpkg.com/pdfjs-dist@4.8.69/build/pdf.worker.min.mjs">
                <Viewer fileUrl={fileUrl} />
              </Worker>
            ) : (
              <div className="flex min-h-[500px] items-center justify-center rounded-2xl border border-dashed border-slate-200 bg-slate-50 text-center">
                <div>
                  <p className="text-lg font-semibold">No PDF loaded</p>
                  <p className="mt-2 text-sm text-slate-500">Upload a file to preview it here.</p>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
