import Image from "next/image";

/**
 * +12 Monkeys brand logo — uses the actual logo from public/.
 * Used in the top-left header and as the app favicon source.
 */
export default function MonkeyIcon({ size = 28, className = "" }: { size?: number; className?: string }) {
  return (
    <Image
      src="/12monkey logo1.png"
      alt="+12 Monkeys logo"
      width={size}
      height={size}
      className={className}
      style={{ objectFit: "contain" }}
      priority
    />
  );
}

