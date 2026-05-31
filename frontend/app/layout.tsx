import type { Metadata } from "next";
import { IBM_Plex_Sans, Space_Grotesk } from "next/font/google";

import "./globals.css";
import { ThemeProvider } from "../components/theme-provider";

const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-display" });
const ibmPlexSans = IBM_Plex_Sans({ subsets: ["latin"], weight: ["400", "500", "600", "700"], variable: "--font-body" });

export const metadata: Metadata = {
  title: "ResumeAgent",
  description: "AI resume optimization platform",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning className={`${spaceGrotesk.variable} ${ibmPlexSans.variable}`}>
      <body className="min-h-screen bg-background text-foreground antialiased">
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem disableTransitionOnChange>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
