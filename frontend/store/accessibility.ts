import { create } from "zustand";
import { persist } from "zustand/middleware";

export type FontScale = "normal" | "large" | "xlarge";

type AccessibilityState = {
  fontScale: FontScale;
  highContrast: boolean;
  reduceMotion: boolean;
  setFontScale: (scale: FontScale) => void;
  toggleHighContrast: () => void;
  toggleReduceMotion: () => void;
  reset: () => void;
};

export const useAccessibilityStore = create<AccessibilityState>()(
  persist(
    (set) => ({
      fontScale: "normal",
      highContrast: false,
      reduceMotion: false,
      setFontScale: (fontScale) => set({ fontScale }),
      toggleHighContrast: () => set((state) => ({ highContrast: !state.highContrast })),
      toggleReduceMotion: () => set((state) => ({ reduceMotion: !state.reduceMotion })),
      reset: () => set({ fontScale: "normal", highContrast: false, reduceMotion: false })
    }),
    { name: "a11y-settings" }
  )
);
