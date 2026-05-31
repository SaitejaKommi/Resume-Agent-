"use client"

import React from "react"

import { cn } from "@/lib/utils"

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "default" | "ghost" | "outline" | "secondary"
  size?: "sm" | "md" | "lg"
  href?: string
}

export function Button({ variant = "default", size = "md", className = "", children, href, ...rest }: Props) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-full font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50"
  const sizes: Record<string, string> = { sm: "h-9 px-4 text-sm", md: "h-11 px-5 text-sm", lg: "h-12 px-6 text-base" }
  const variants: Record<string, string> = {
    default: "bg-emerald-500 text-slate-950 hover:bg-emerald-400 shadow-[0_18px_40px_-18px_rgba(16,185,129,0.9)]",
    secondary: "bg-slate-950 text-white hover:bg-slate-800",
    ghost: "bg-transparent text-slate-200 hover:bg-white/8 hover:text-white",
    outline: "border border-white/12 bg-white/5 text-white hover:bg-white/10",
  }

  const classNames = cn(base, sizes[size], variants[variant], className)

  if (href) {
    return (
      <a href={href} className={classNames} {...(rest as React.AnchorHTMLAttributes<HTMLAnchorElement>)}>
        {children}
      </a>
    )
  }

  return (
    <button className={classNames} {...rest}>
      {children}
    </button>
  )
}

export default Button

