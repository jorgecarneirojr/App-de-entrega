import type { Metadata } from "next";
import "leaflet/dist/leaflet.css";
import "./globals.css";

import { Providers } from "@/components/providers";
import { RouteAnnouncer } from "@/components/route-announcer";

export const metadata: Metadata = {
  title: {
    default: "App de Entrega",
    template: "%s | App de Entrega"
  },
  description: "Aplicacao de delivery full stack com cliente, restaurante e entregador.",
  keywords: ["delivery", "next.js", "fastapi", "projeto integrador", "app de entrega"]
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>
        <a href="#conteudo" className="skip-link">
          Pular para o conteudo
        </a>
        <RouteAnnouncer />
        <div id="conteudo">
          <Providers>{children}</Providers>
        </div>
      </body>
    </html>
  );
}
