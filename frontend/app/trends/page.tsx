"use client"

import { useEffect, useState } from "react"

export default function Trends() {
  const [trends,setTrends] = useState<any[]>([])

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/trends")
      .then(res => res.json())
      .then(data => setTrends(data))
  }, [])

  return (
    <div style={{padding:40}}>
      <h1>AI Trend Detection</h1>

      {trends.map((t,i) => (
        <div key={i}>
          <p>{t.insight_text}</p>
        </div>
      ))}
    </div>
  )
}