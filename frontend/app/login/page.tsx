'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { API_URL } from '@/lib/api'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()
  async function login(e: React.FormEvent) {
    e.preventDefault()
    const res = await fetch(`${API_URL}/api/auth/login`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email, password}) })
    if(!res.ok) return alert('Invalid credentials')
    const data = await res.json(); localStorage.setItem('token', data.access_token); router.push('/admin')
  }
  return <form onSubmit={login} className="bg-white p-4 rounded space-y-3"><h1 className="text-2xl">Admin Login</h1><input className="border p-2 w-full" type="email" onChange={e=>setEmail(e.target.value)} /><input className="border p-2 w-full" type="password" onChange={e=>setPassword(e.target.value)} /><button className="bg-brandBlue text-white px-4 py-2 rounded">Login</button></form>
}
