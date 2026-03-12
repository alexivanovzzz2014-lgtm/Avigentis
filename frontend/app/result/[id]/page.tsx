import { API_URL } from '@/lib/api'

export default async function ResultPage({ params }: { params: { id: string } }) {
  const res = await fetch(`${API_URL}/api/scans/${params.id}`, { cache: 'no-store' })
  const data = await res.json()
  return <div className="space-y-3 bg-white p-4 rounded"><h1 className="text-2xl font-bold">Scan Result</h1><p>Status: <strong>{data.status}</strong></p><p>Score: <strong>{data.score}</strong></p><pre className="bg-brandLight p-3 whitespace-pre-wrap">{data.public_summary}</pre></div>
}
