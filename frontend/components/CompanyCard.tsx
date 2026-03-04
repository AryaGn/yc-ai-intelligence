import Link from "next/link";

export default function CompanyCard({ company }: any) {
  return (
    <div style={{ border: "1px solid #ccc", padding: 20, margin: 10 }}>
      <h3>{company.name}</h3>
      <p>{company.summary}</p>
      <Link href={`/companies/${company.id}`}>
        View Profile
      </Link>
    </div>
  );
}