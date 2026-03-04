"use client"

import { useEffect, useState } from "react"

export default function Companies() {

  const [companies, setCompanies] = useState<any[]>([])

  useEffect(() => {
    fetch("http://localhost:8000/api/companies")
      .then(res => res.json())
      .then(data => setCompanies(data))
  }, [])

  return (
    <main style={{ padding: 40 }}>
      <h1>YC Companies</h1>

      {companies.map((c:any) => (
        <div key={c.id}>{c.name}</div>
      ))}

    </main>
  )
}
