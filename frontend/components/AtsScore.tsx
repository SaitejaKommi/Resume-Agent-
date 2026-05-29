"use client"
import React from "react"

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
  const color = normalized > 75 ? "#16a34a" : normalized > 50 ? "#f59e0b" : "#ef4444"

  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
      <svg width="100" height="100" viewBox="0 0 100 100">
        <g transform="translate(50,50)">
          <circle r={r} stroke="#e5e7eb" strokeWidth={stroke} fill="none" />
          <circle r={r} stroke={color} strokeWidth={stroke} fill="none" strokeDasharray={`${dash} ${c - dash}`} strokeLinecap="round" transform="rotate(-90)" />
          <text x="0" y="6" textAnchor="middle" fontSize="18" fill="currentColor">{Math.round(normalized)}</text>
        </g>
      </svg>
      <div className="mt-3">
        {missingKeywords.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {missingKeywords.map((k) => (
              <span key={k} className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">{k}</span>
            ))}
          </div>
        )}
        <ul className="mt-3 list-disc ml-5 text-sm text-gray-600 dark:text-gray-300">
          {suggestions.map((s) => <li key={s}>{s}</li>)}
        </ul>
      </div>
    </div>
  )
}
