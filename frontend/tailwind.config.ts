import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: "hsl(var(--card))",
        cardForeground: "hsl(var(--card-foreground))",
        accent: "hsl(var(--accent))",
        accentForeground: "hsl(var(--accent-foreground))",
        muted: "hsl(var(--muted))",
        mutedForeground: "hsl(var(--muted-foreground))",
        border: "hsl(var(--border))",
      },
      fontFamily: {
        display: ["var(--font-display)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
      },
      boxShadow: {
        glow: "0 25px 80px -20px rgba(15, 23, 42, 0.45)",
      },
      backgroundImage: {
        "hero-grid": "radial-gradient(circle at 1px 1px, rgba(15,23,42,0.12) 1px, transparent 0)",
      },
    },
  },
  plugins: [],
};

export default config;
