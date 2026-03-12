import './globals.css'
import Link from 'next/link'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="bg-brandDark text-white p-4 flex gap-4">
          <Link href="/">Avigentis</Link>
          <Link href="/scan">Scan</Link>
          <Link href="/admin">Admin</Link>
        </header>
        <main className="max-w-4xl mx-auto p-4">{children}</main>
      </body>
    </html>
  )
}
