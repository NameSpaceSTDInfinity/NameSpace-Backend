import React from 'react';
import MinistryCard from '../components/MinistryCard';

const ministries = [
  {
    name: "",
    description: "GAIL (Gas Authority Of India Ltd.) is India’s largest state-owned natural gas company, handling transportation, distribution, and marketing of natural gas nationwide.",
    logo: "/Gail.png",
    link: "https://www.gailonline.com"
  },
  {
    name: "",
    description: "Ministry of Petroleum and Natural Gas (MoPNG): The Ministry formulates policies for exploration, production, refining, and distribution of petroleum, natural gas, and related products in India. It oversees energy security, regulating oil companies, promoting renewable energy integration, and managing energy pricing and import strategies to meet the nation’s growing energy demands.                                                                                                                      ",
    logo: "/images.png",
    link: "https://mopng.gov.in/en"
  },
  
];

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24 bg-sky-100">
      <nav className="w-full bg-white p-4 mb-8">
        <h1 className="text-2xl font-bold">SIH  Problem Statement 1706</h1>
      </nav>
      <div className="flex justify-center items-center space-x-8 p-8">
        {ministries.map((ministry, index) => (
          <MinistryCard key={index} ministry={ministry} />
        ))}
      </div>
    </main>
  );
}