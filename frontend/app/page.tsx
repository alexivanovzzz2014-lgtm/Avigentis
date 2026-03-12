import Link from 'next/link'

export default function Home() {
  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">Avigentis Cyber Readiness Scanner</h1>
      <p>Supports readiness assessment using publicly visible indicators for NIS2 / ЗКС support for achieving compliance.</p>
      <p className="text-sm bg-white p-3 rounded">Скенерът анализира само публично достъпна информация. Резултатът е предварителен и не представлява официален одит, правно становище или гаранция за съответствие.</p>
      <Link className="bg-brandBlue text-white px-4 py-2 rounded inline-block" href="/scan">Start preliminary analysis</Link>
    </div>
  )
}
