"use client"

import React from "react"

import { cn } from "@/lib/utils"

type Props = { children: React.ReactNode; variant?: "default" | "success" | "warning" | "destructive" }

export function Badge({ children, variant = "default" }: Props) {
  const classes = {
    default: "border border-white/12 bg-white/10 text-slate-100",
    success: "border border-emerald-400/20 bg-emerald-400/12 text-emerald-200",
    warning: "border border-amber-400/20 bg-amber-400/12 text-amber-200",
    destructive: "border border-rose-400/20 bg-rose-400/12 text-rose-200",
  }

  return <span className={cn("inline-flex items-center rounded-full px-3 py-1 text-xs font-medium", classes[variant])}>{children}</span>
}

export default Badge
