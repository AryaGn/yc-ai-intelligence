export default function ScoreCard({ label, score }: any) {
  return (
    <div style={{ border: "1px solid #000", padding: 20 }}>
      <h4>{label}</h4>
      <p style={{ fontSize: 24 }}>{score}</p>
    </div>
  );
}