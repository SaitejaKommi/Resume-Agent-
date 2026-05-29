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
