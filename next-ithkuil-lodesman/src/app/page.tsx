import TextCard, { TextCardProps } from "@/components/TextCard";
import Image from "next/image";

export default function Home() {
  const data: TextCardProps[] = [{
    text: "The diddle, oil up little brother",
    title: "Hello World"
  }, {
    text: "I am the worst, I am the biggest, I am the strongest",
    title: "I am the worst"
  }]

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <span>Your Quotes</span>
        {data.map((d, i) => <TextCard key={i} {...d} />)}
      </main>

    </div>
  );
}
