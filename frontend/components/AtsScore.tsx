"use client"

import React from "react"

import { Badge } from "./ui/badge"

type Props = {
  score: number
  missingKeywords: string[]
  suggestions: string[]
}

export default function AtsScore({ score, missingKeywords, suggestions }: Props) {
  const radius = 36
  const stroke = 8
  const normalized = Math.max(0, Math.min(100, score))
  const r = radius
  const c = 2 * Math.PI * r
  const dash = (normalized / 100) * c
  const color = normalized > 75 ? "#34d399" : normalized > 50 ? "#fbbf24" : "#fb7185"

  return (
    <div className="rounded-[1.5rem] border border-white/10 bg-white/6 p-5 text-white shadow-[0_28px_80px_-30px_rgba(2,6,23,0.65)] backdrop-blur-xl">
      <div className="flex items-center gap-5">
        <svg width="112" height="112" viewBox="0 0 100 100">
          <g transform="translate(50,50)">
            <circle r={r} stroke="rgba(255,255,255,0.14)" strokeWidth={stroke} fill="none" />
            <circle r={r} stroke={color} strokeWidth={stroke} fill="none" strokeDasharray={`${dash} ${c - dash}`} strokeLinecap="round" transform="rotate(-90)" />
            <text x="0" y="6" textAnchor="middle" fontSize="18" fill="currentColor">{Math.round(normalized)}</text>
          </g>
        </svg>
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">ATS score</p>
          <p className="mt-2 max-w-xs text-sm leading-6 text-slate-300">A quick read on how closely the resume matches the role and where it can be tightened.</p>
        </div>
      </div>
      <div className="mt-5 space-y-4">
        {missingKeywords.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {missingKeywords.map((k) => (
              <Badge key={k} variant="warning">
                {k}
              </Badge>
            ))}
          </div>
        )}
        <ul className="space-y-2 text-sm text-slate-300">
          {suggestions.map((s) => (
            <li key={s} className="flex gap-3">
              <span className="mt-2 h-1.5 w-1.5 rounded-full bg-emerald-400" />
              <span>{s}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
