export default function TrendCard({ trend }: any) {
  return (
    <div style={{ border: "1px solid blue", padding: 20, margin: 10 }}>
      <h3>{trend.title}</h3>
      <p>{trend.description}</p>
      <p>Confidence: {trend.confidence}</p>
    </div>
  );
}