"use client";

import { useState } from "react";
import { askQuestion } from "@/lib/api";

export default function ConsolePage() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<any>(null);

  async function handleAsk() {
    const result = await askQuestion(question);
    setResponse(result);
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>AI Research Console</h1>

      <input
        style={{ width: 400, padding: 10 }}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask anything about YC companies..."
      />

      <button onClick={handleAsk}>Ask</button>

      {response && (
        <div style={{ marginTop: 20 }}>
          <h3>Answer</h3>
          <p>{response.answer}</p>

          <h4>Cited Companies</h4>
          <ul>
            {response.companies.map((c: any) => (
              <li key={c.id}>{c.name}</li>
            ))}
          </ul>

          <h4>Reasoning Trace</h4>
          <p>{response.reasoning_trace}</p>
        </div>
      )}
    </div>
  );
}