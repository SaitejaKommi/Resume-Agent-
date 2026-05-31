"use client"
import React, { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { uploadResume } from "../lib/api"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { Button } from "./ui/button"
import { Badge } from "./ui/badge"

type Props = { onDone: (resumeId: number) => void }

export default function ResumeUploader({ onDone }: Props) {
  const [error, setError] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setError(null)
    if (!acceptedFiles || acceptedFiles.length === 0) return
    const file = acceptedFiles[0]
    if (file.size > 5 * 1024 * 1024) { setError('File too large (max 5MB)'); return }
    setUploading(true)
    try {
      const res = await uploadResume(file)
      onDone(res.resume_id)
    } catch (err) {
      setError('Upload failed')
    } finally { setUploading(false) }
  }, [onDone])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'] }, maxFiles: 1 })

  return (
    <Card className="border-white/10 bg-white/6">
      <CardHeader>
        <div className="flex items-center justify-between gap-3">
          <div>
            <CardTitle>Resume upload</CardTitle>
            <CardDescription>Upload a PDF or DOCX and we’ll use it as the base for tailoring.</CardDescription>
          </div>
          <Badge variant="default">Max 5 MB</Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div
          {...getRootProps()}
          className={`group rounded-[1.5rem] border border-dashed p-8 text-center transition-all ${isDragActive ? "border-emerald-400 bg-emerald-400/10" : "border-white/12 bg-white/5 hover:border-emerald-300/50 hover:bg-white/10"}`}
        >
          <input {...getInputProps()} />
          <p className="text-lg font-medium text-white">{isDragActive ? "Drop the file here" : "Drag and drop your resume"}</p>
          <p className="mt-2 text-sm text-slate-300">PDF and DOCX are supported. Click anywhere in this panel to browse.</p>
        </div>
        <div className="flex items-center gap-3 text-sm text-slate-300">
          {uploading ? <Badge variant="success">Uploading</Badge> : <Badge variant="default">Ready</Badge>}
          <span>{error ?? "Your file is uploaded securely to the backend."}</span>
        </div>
        {error && <p className="text-sm text-rose-300">{error}</p>}
        <div className="flex justify-end">
          <Button variant="outline" size="sm" disabled>
            Preview enabled after upload
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
