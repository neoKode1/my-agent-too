/**
 * +12 Monkeys brand icon — minimal monkey face silhouette.
 * Used in the top-left header and as the app favicon source.
 */
export default function MonkeyIcon({ size = 28, className = "" }: { size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Left ear */}
      <circle cx="12" cy="22" r="10" fill="#6C63FF" opacity="0.85" />
      <circle cx="12" cy="22" r="6" fill="#0D0D0D" />
      {/* Right ear */}
      <circle cx="52" cy="22" r="10" fill="#6C63FF" opacity="0.85" />
      <circle cx="52" cy="22" r="6" fill="#0D0D0D" />
      {/* Head */}
      <ellipse cx="32" cy="34" rx="20" ry="22" fill="#6C63FF" />
      {/* Face / muzzle area */}
      <ellipse cx="32" cy="40" rx="12" ry="10" fill="#1A1A1A" />
      {/* Left eye */}
      <ellipse cx="24" cy="30" rx="3.5" ry="4" fill="#0D0D0D" />
      <ellipse cx="24.5" cy="29.5" rx="1.5" ry="2" fill="#E8E8E8" />
      {/* Right eye */}
      <ellipse cx="40" cy="30" rx="3.5" ry="4" fill="#0D0D0D" />
      <ellipse cx="40.5" cy="29.5" rx="1.5" ry="2" fill="#E8E8E8" />
      {/* Nostrils */}
      <circle cx="28" cy="40" r="2" fill="#0D0D0D" />
      <circle cx="36" cy="40" r="2" fill="#0D0D0D" />
      {/* Subtle mouth line */}
      <path d="M28 45 Q32 48 36 45" stroke="#0D0D0D" strokeWidth="1.5" fill="none" strokeLinecap="round" />
    </svg>
  );
}

