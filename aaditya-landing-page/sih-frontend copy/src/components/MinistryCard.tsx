"use client";
import React from 'react';
import { Card, CardBody, CardHeader,Button } from "@nextui-org/react";
import { useRouter } from 'next/navigation';
interface MinistryProps {
  ministry: {
    name: string;
    description: string;
    logo: string; 
    link: string;
  }
}


const MinistryCard: React.FC<MinistryProps> = ({ ministry }) => {
  const router = useRouter(); // Initialize useRouter

  const handleClick = () => {
    router.push(ministry.link); // Navigate to the provided link
  };
  return (
    <Card className="max-w-md bg-white shadow-lg rounded-lg overflow-hidden">
      <CardHeader className="flex gap-3 p-4">
        <img src={ministry.logo} alt={`${ministry.name} logo`} className="w-18 h-17" />
        <div className="flex flex-col">
          <p className="text-lg font-semibold">{ministry.name}</p>
        </div>
      </CardHeader>
      <CardBody className="p-4">
        <p className="text-sm mb-4">{ministry.description}</p>
        
        <Button variant="flat" className="bg-gray-200 text-gray-800 cursor-pointer" onClick={handleClick}>
          More information
        </Button>
          
      </CardBody>
    </Card>
  );
}

export default MinistryCard;