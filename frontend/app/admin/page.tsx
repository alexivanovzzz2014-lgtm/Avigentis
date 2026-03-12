'use client'
import { useEffect, useState } from 'react'
import { API_URL } from '@/lib/api'

export default function AdminPage() {
  const [scans, setScans] = useState<any[]>([])
  const [status, setStatus] = useState('')
  const [orgType, setOrgType] = useState('')
  async function load() {
    const token = localStorage.getItem('token')
    const params = new URLSearchParams(); if(status) params.set('status', status); if(orgType) params.set('organization_type', orgType)
    const res = await fetch(`${API_URL}/api/admin/scans?${params.toString()}`, { headers: { Authorization: `Bearer ${token}` } })
    if(res.ok) setScans(await res.json())
  }
  useEffect(()=>{load()},[])
  return <div className="space-y-3"><h1 className="text-2xl font-bold">Admin dashboard</h1><div className="flex gap-2"><input className="border p-2" placeholder="Status filter" value={status} onChange={e=>setStatus(e.target.value)} /><input className="border p-2" placeholder="Org type filter" value={orgType} onChange={e=>setOrgType(e.target.value)} /><button className="bg-brandBlue text-white px-3 rounded" onClick={load}>Apply</button></div>{scans.map(s => <div key={s.id} className="bg-white p-3 rounded"><div className="font-semibold">{s.normalized_domain} | {s.score} | {s.status}</div><details><summary>Public summary</summary><pre className="whitespace-pre-wrap">{s.public_summary}</pre></details><details><summary>Internal summary</summary><pre className="whitespace-pre-wrap">{s.internal_summary}</pre></details><details><summary>Raw JSON</summary><pre className="overflow-auto">{JSON.stringify(s.raw_scan_results, null, 2)}</pre></details></div>)}</div>
}
