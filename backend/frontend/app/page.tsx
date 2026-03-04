"use client"

import { useState } from "react"

export default function Home() {

  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState<any>(null)

  async function ask() {

    const res = await fetch("http://127.0.0.1:8000/api/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    })

    const data = await res.json()
    setAnswer(data)
  }

  return (
    <main style={{ padding: 40 }}>

      <h1>YC AI Intelligence System</h1>

      <h2>AI Research Console</h2>

      <input
        style={{ padding: 10, width: 400 }}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask about YC companies..."
      />

      <button
        style={{ marginLeft: 10, padding: 10 }}
        onClick={ask}
      >
        Ask
      </button>

      {answer && (
        <div style={{ marginTop: 20 }}>
          <h3>Answer</h3>
          <p>{answer.answer}</p>

          <h3>Companies</h3>

          {answer.companies.map((c:any) => (
            <div key={c.id}>{c.name}</div>
          ))}
        </div>
      )}

    </main>
  )
}
