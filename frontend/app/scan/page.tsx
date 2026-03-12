'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { API_URL } from '@/lib/api'

export default function ScanPage() {
  const [form, setForm] = useState<any>({ organization_type: 'Municipality' })
  const router = useRouter()
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const res = await fetch(`${API_URL}/api/scans`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
    if (res.ok) { const data = await res.json(); router.push(`/result/${data.id}`) } else alert('Could not create scan request')
  }
  return <form onSubmit={submit} className="space-y-3 bg-white p-4 rounded"><h1 className="text-2xl font-bold">Preliminary readiness scan</h1><input className="border p-2 w-full" placeholder="Domain (example.bg)" required onChange={e=>setForm({...form,domain:e.target.value})} /><input className="border p-2 w-full" placeholder="Email" type="email" required onChange={e=>setForm({...form,email:e.target.value})} /><input className="border p-2 w-full" placeholder="Organization name" onChange={e=>setForm({...form,organization_name:e.target.value})} /><select className="border p-2 w-full" onChange={e=>setForm({...form,organization_type:e.target.value})}>{['Municipality','Public institution','Public sector organization','Critical infrastructure operator','Other'].map(v=><option key={v}>{v}</option>)}</select><input className="border p-2 w-full" placeholder="Phone" onChange={e=>setForm({...form,phone:e.target.value})} /><label className="flex gap-2"><input type="checkbox" required onChange={e=>setForm({...form,gdpr_consent:e.target.checked})}/>GDPR consent</label><label className="flex gap-2"><input type="checkbox" required onChange={e=>setForm({...form,public_info_acknowledgment:e.target.checked})}/>I acknowledge publicly accessible information only.</label><label className="flex gap-2"><input type="checkbox" onChange={e=>setForm({...form,request_consultation:e.target.checked})}/>Request consultation</label><p className="text-xs">Not a pentest, not a formal audit, not a legal opinion. Avigentis is a consultant, not a guarantor.</p><button className="bg-brandBlue text-white px-4 py-2 rounded" type="submit">Run scan</button></form>
}
