"use client";
import type React from "react";
import { Button } from "@/components/ui/button"


export interface TextCardProps {
  text: string;
 
  title: string;
 
}

const TextCard: React.FC<TextCardProps> = ({

  title,
  text,
 
}) => {
  return (
    <div className="flex w-full gap-2 min-w-64 max-w-[50rem]">
     
      <div className="flex flex-col gap-2">
        <h1 className="text-lg font-bold">{title}</h1>
        <p className="text-sm">{text}</p>
      </div>
 
    </div>
  );
};

export default TextCard;