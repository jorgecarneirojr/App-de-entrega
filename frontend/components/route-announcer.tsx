"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const routeLabels: Record<string, string> = {
  "/": "Início",
  "/acessibilidade": "Acessibilidade",
  "/cart": "Carrinho",
  "/courier": "Painel do entregador",
  "/login": "Login",
  "/orders": "Meus pedidos",
  "/owner": "Painel do restaurante",
  "/register": "Cadastro"
};

function labelFor(pathname: string) {
  if (routeLabels[pathname]) {
    return routeLabels[pathname];
  }
  if (pathname.startsWith("/restaurants/")) {
    return "Cardápio do restaurante";
  }
  return "Página";
}

export function RouteAnnouncer() {
  const pathname = usePathname();
  const [message, setMessage] = useState("");

  useEffect(() => {
    setMessage(`Página atual: ${labelFor(pathname)}`);
  }, [pathname]);

  return (
    <div className="sr-only" aria-live="polite" aria-atomic="true">
      {message}
    </div>
  );
}
