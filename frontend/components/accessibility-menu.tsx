"use client";

import Link from "next/link";
import { useState } from "react";

import { useAccessibilityStore } from "@/store/accessibility";

export function AccessibilityMenu() {
  const [open, setOpen] = useState(false);
  const fontScale = useAccessibilityStore((state) => state.fontScale);
  const highContrast = useAccessibilityStore((state) => state.highContrast);
  const reduceMotion = useAccessibilityStore((state) => state.reduceMotion);
  const setFontScale = useAccessibilityStore((state) => state.setFontScale);
  const toggleHighContrast = useAccessibilityStore((state) => state.toggleHighContrast);
  const toggleReduceMotion = useAccessibilityStore((state) => state.toggleReduceMotion);
  const reset = useAccessibilityStore((state) => state.reset);

  return (
    <div
      className="relative"
      onKeyDown={(event) => {
        if (event.key === "Escape") {
          setOpen(false);
        }
      }}
    >
      <button
        type="button"
        className="rounded-lg border border-red-200 px-3 py-1 transition hover:border-red-300 hover:bg-red-50"
        aria-expanded={open}
        aria-controls="a11y-panel"
        onClick={() => setOpen((current) => !current)}
      >
        Acessibilidade
      </button>

      {open && (
        <div
          id="a11y-panel"
          role="group"
          aria-label="Recursos de acessibilidade"
          className="absolute right-0 z-50 mt-2 w-72 rounded-2xl border border-red-100 bg-white p-4 text-left shadow-xl"
        >
          <p className="text-sm font-bold text-slate-900">Ajustes de leitura</p>

          <div role="group" aria-label="Tamanho do texto" className="mt-2 flex gap-2">
            <button
              type="button"
              aria-pressed={fontScale === "normal"}
              aria-label="Tamanho de texto normal"
              className="rounded-lg border border-red-200 px-3 py-1 text-sm"
              onClick={() => setFontScale("normal")}
            >
              A
            </button>
            <button
              type="button"
              aria-pressed={fontScale === "large"}
              aria-label="Aumentar tamanho do texto"
              className="rounded-lg border border-red-200 px-3 py-1 text-sm"
              onClick={() => setFontScale("large")}
            >
              A+
            </button>
            <button
              type="button"
              aria-pressed={fontScale === "xlarge"}
              aria-label="Aumentar mais o tamanho do texto"
              className="rounded-lg border border-red-200 px-3 py-1 text-sm"
              onClick={() => setFontScale("xlarge")}
            >
              A++
            </button>
          </div>

          <div className="mt-3 grid gap-2">
            <button
              type="button"
              aria-pressed={highContrast}
              className="rounded-lg border border-red-200 px-3 py-2 text-left text-sm"
              onClick={toggleHighContrast}
            >
              Alto contraste
            </button>
            <button
              type="button"
              aria-pressed={reduceMotion}
              className="rounded-lg border border-red-200 px-3 py-2 text-left text-sm"
              onClick={toggleReduceMotion}
            >
              Reduzir movimento
            </button>
            <button type="button" className="rounded-lg border border-red-200 px-3 py-2 text-left text-sm" onClick={reset}>
              Restaurar padrão
            </button>
          </div>

          <Link href="/acessibilidade" className="mt-3 inline-block text-sm font-semibold text-red-700 underline">
            Sobre os recursos de acessibilidade
          </Link>
        </div>
      )}
    </div>
  );
}
