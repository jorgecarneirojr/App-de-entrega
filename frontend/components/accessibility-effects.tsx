"use client";

import { useEffect } from "react";

import { useAccessibilityStore } from "@/store/accessibility";

export function AccessibilityEffects() {
  const fontScale = useAccessibilityStore((state) => state.fontScale);
  const highContrast = useAccessibilityStore((state) => state.highContrast);
  const reduceMotion = useAccessibilityStore((state) => state.reduceMotion);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.toggle("a11y-font-lg", fontScale === "large");
    root.classList.toggle("a11y-font-xl", fontScale === "xlarge");
    root.classList.toggle("a11y-high-contrast", highContrast);
    root.classList.toggle("a11y-reduce-motion", reduceMotion);
  }, [fontScale, highContrast, reduceMotion]);

  return null;
}
