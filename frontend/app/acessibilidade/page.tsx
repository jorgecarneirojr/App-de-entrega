import type { Metadata } from "next";
import Link from "next/link";

import { Header } from "@/components/header";

export const metadata: Metadata = {
  title: "Acessibilidade",
  description: "Recursos de acessibilidade da plataforma App de Entrega."
};

const recursos = [
  "Estrutura semântica com títulos hierárquicos, marcos de navegação e idioma português do Brasil.",
  "Atalho “Pular para o conteúdo” e foco visível em todos os controles.",
  "Formulários com rótulos associados, autocomplete e mensagens de status anunciadas.",
  "Anúncio automático da mudança de página para leitores de tela.",
  "Ajuste de tamanho do texto em três níveis (A, A+ e A++).",
  "Modo de alto contraste e opção de reduzir movimento.",
  "Mapa com resumo textual da rota, distância e tempo, além de marcadores com título.",
  "Layout responsivo, verificado em largura de 390 px sem rolagem horizontal."
];

export default function AccessibilityPage() {
  return (
    <main>
      <Header />
      <section className="container-box max-w-4xl space-y-5">
        <div className="glass-panel px-6 py-6">
          <span className="badge">Compromisso</span>
          <h1 className="mt-3 text-3xl font-black text-red-700">Acessibilidade</h1>
          <p className="mt-3 text-slate-600">
            A plataforma foi construída para ser utilizável por pessoas com diferentes necessidades,
            incluindo navegação por teclado, leitores de tela e ajustes visuais. As decisões seguem
            boas práticas alinhadas às diretrizes WCAG 2 níveis A e AA.
          </p>
        </div>

        <div className="card space-y-4">
          <h2 className="text-xl font-black text-red-700">Como usar os ajustes</h2>
          <p className="text-slate-600">
            No topo de todas as páginas, o botão <strong>Acessibilidade</strong> abre um painel com
            controle de tamanho do texto, alto contraste, redução de movimento e restauração dos
            padrões. As preferências ficam salvas no navegador.
          </p>
        </div>

        <div className="card space-y-4">
          <h2 className="text-xl font-black text-red-700">Recursos implementados</h2>
          <ul className="list-disc space-y-2 pl-5 text-slate-600">
            {recursos.map((recurso) => (
              <li key={recurso}>{recurso}</li>
            ))}
          </ul>
        </div>

        <div className="card space-y-4">
          <h2 className="text-xl font-black text-red-700">Avaliação</h2>
          <p className="text-slate-600">
            A interface foi avaliada com a ferramenta automatizada axe-core, considerando as regras
            WCAG 2 níveis A e AA. Não foram identificadas violações nas telas de vitrine, login,
            cadastro, cardápio, carrinho, painel do restaurante e painel do entregador.
          </p>
          <p className="text-sm text-slate-500">
            A auditoria automatizada é um indicativo de qualidade e não substitui testes manuais com
            leitores de tela, navegação apenas por teclado ou avaliação com usuários.
          </p>
        </div>

        <div className="card space-y-4">
          <h2 className="text-xl font-black text-red-700">Limitações conhecidas</h2>
          <ul className="list-disc space-y-2 pl-5 text-slate-600">
            <li>O mapa é um complemento visual; a rota também é descrita em texto.</li>
            <li>Não há testes automatizados com leitores de tela.</li>
            <li>A validação com usuários foi restrita ao contexto do projeto.</li>
          </ul>
        </div>

        <div className="card space-y-3">
          <h2 className="text-xl font-black text-red-700">Contato</h2>
          <p className="text-slate-600">
            Para relatar barreiras de acessibilidade ou sugerir melhorias, abra uma issue no
            repositório do projeto.
          </p>
          <p>
            <a
              className="font-semibold text-red-700 underline"
              href="https://github.com/jorgecarneirojr/App-de-entrega/issues"
            >
              github.com/jorgecarneirojr/App-de-entrega/issues
            </a>
          </p>
          <Link href="/" className="btn-primary inline-flex">
            Voltar ao início
          </Link>
        </div>
      </section>
    </main>
  );
}
