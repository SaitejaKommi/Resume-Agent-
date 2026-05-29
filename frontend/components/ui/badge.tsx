"use client"
import React from "react"

type Props = { children: React.ReactNode, variant?: 'default' | 'success' | 'warning' | 'destructive' }

export function Badge({ children, variant='default' }: Props) {
  const classes = {
    default: 'bg-gray-100 text-gray-800 px-2 py-1 rounded',
    success: 'bg-green-100 text-green-800 px-2 py-1 rounded',
    warning: 'bg-amber-100 text-amber-800 px-2 py-1 rounded',
    destructive: 'bg-red-100 text-red-800 px-2 py-1 rounded',
  }
  return <span className={classes[variant]}>{children}</span>
}

export default Badge
