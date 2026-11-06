"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { AccessibilityMenu } from "@/components/accessibility-menu";

import { useAuthStore } from "@/store/auth";
import { useCartStore } from "@/store/cart";

export function Header() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const cartCount = useCartStore((state) => state.items.reduce((total, item) => total + item.quantity, 0));
  const pathname = usePathname();
  const isActive = (href: string) => (href === "/" ? pathname === "/" : pathname.startsWith(href));

  return (
    <header className="container-box relative z-40">
      <nav aria-label="Navegacao principal" className="glass-panel flex flex-col gap-4 px-5 py-4 md:flex-row md:items-center md:justify-between">
        <div>
          <Link href="/" className="text-xl font-black tracking-tight text-red-700">
            Entrega PI II
          </Link>
          <p className="text-sm text-slate-500">Delivery full stack com descoberta, pedido e acompanhamento.</p>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-sm font-medium">
          <Link href="/" aria-current={isActive("/") ? "page" : undefined}>Inicio</Link>
          <Link href="/cart" aria-current={isActive("/cart") ? "page" : undefined} aria-label={`Carrinho com ${cartCount} itens`} className="inline-flex items-center gap-2 rounded-full border border-red-200 bg-white/80 px-3 py-1.5">
            <span>Carrinho</span>
            <span className="rounded-full bg-red-600 px-2 py-0.5 text-xs font-bold text-white">{cartCount}</span>
          </Link>
          {user && <Link href="/orders" aria-current={isActive("/orders") ? "page" : undefined}>Pedidos</Link>}
          {user?.role === "cliente" && <Link href="/register" aria-current={isActive("/register") ? "page" : undefined}>Conta</Link>}
          {(user?.role === "dono_restaurante" || user?.role === "admin") && <Link href="/owner" aria-current={isActive("/owner") ? "page" : undefined}>Painel Restaurante</Link>}
          {user?.role === "entregador" && <Link href="/courier" aria-current={isActive("/courier") ? "page" : undefined}>Painel Entregador</Link>}
          {!user ? (
            <>
              <Link href="/login" aria-current={isActive("/login") ? "page" : undefined}>Login</Link>
              <Link href="/register" aria-current={isActive("/register") ? "page" : undefined}>Cadastro</Link>
            </>
          ) : (
            <>
              <span className="rounded-full bg-white/80 px-3 py-1 text-slate-500">{user.name}</span>
              <button type="button" className="rounded-lg border border-red-200 px-3 py-1 transition hover:border-red-300 hover:bg-red-50" onClick={logout}>
                Sair
              </button>
            </>
          )}
          <AccessibilityMenu />
        </div>
      </nav>
    </header>
  );
}
