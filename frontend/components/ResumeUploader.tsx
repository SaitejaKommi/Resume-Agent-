"use client"
import React, { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { uploadResume } from "../lib/api"

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
    <div className="mt-4">
      <div {...getRootProps()} className={`p-6 border-2 border-dashed rounded text-center ${isDragActive? 'border-blue-400':''}`}>
        <input {...getInputProps()} />
        {isDragActive ? <p>Drop the file here ...</p> : <p>Drag & drop a PDF or DOCX here, or click to select</p>}
      </div>
      {uploading && <div className="mt-2">Uploading...</div>}
      {error && <div className="mt-2 text-red-600">{error}</div>}
    </div>
  )
}
