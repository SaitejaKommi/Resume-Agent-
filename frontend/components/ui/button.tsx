"use client"
import React from "react"

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'default' | 'ghost' | 'outline' | 'destructive' | 'success' | 'warning', size?: 'sm' | 'md' | 'lg' }

export function Button({ variant='default', size='md', className='', children, ...rest }: Props) {
  const base = 'inline-flex items-center justify-center rounded-md font-medium transition-colors'
  const sizes: Record<string,string> = { sm: 'px-2 py-1 text-sm', md: 'px-3 py-2 text-sm', lg: 'px-4 py-2 text-base' }
  const variants: Record<string,string> = {
    default: 'bg-blue-600 text-white hover:bg-blue-700',
    ghost: 'bg-transparent text-gray-700 dark:text-gray-200',
    outline: 'border border-gray-200 dark:border-gray-700',
    destructive: 'bg-red-600 text-white',
    success: 'bg-green-600 text-white',
    warning: 'bg-amber-500 text-white'
  }
  return <button className={`${base} ${sizes[size]} ${variants[variant]} ${className}`} {...rest}>{children}</button>
}

export default Button
import * as React from "react";

import { cn } from "@/lib/utils";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "default" | "secondary" | "outline";
  size?: "sm" | "default" | "lg";
  href?: string;
};

const variantClasses: Record<NonNullable<ButtonProps["variant"]>, string> = {
  default: "bg-emerald-600 text-white shadow-glow hover:bg-emerald-700",
  secondary: "bg-slate-900 text-white hover:bg-slate-800",
  outline: "border border-slate-200 bg-white text-slate-900 hover:bg-slate-50",
};

const sizeClasses: Record<NonNullable<ButtonProps["size"]>, string> = {
  sm: "h-9 px-3 text-sm",
  default: "h-11 px-5 text-sm",
  lg: "h-12 px-6 text-base",
};

export function Button({ className, variant = "default", size = "default", href, ...props }: ButtonProps) {
  const sharedClassName = cn(
    "inline-flex items-center justify-center gap-2 rounded-full font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    variantClasses[variant],
    sizeClasses[size],
    className,
  );

  if (href) {
    return <a className={sharedClassName} href={href} {...(props as React.AnchorHTMLAttributes<HTMLAnchorElement>)} />;
  }

  return <button className={sharedClassName} {...props} />;
}
