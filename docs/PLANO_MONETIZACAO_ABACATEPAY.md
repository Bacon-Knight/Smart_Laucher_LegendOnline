# 🥑 Plano Estratégico de Monetização e Rentabilidade — AbacatePay

---

## 📌 1. Visão Geral

Este documento descreve a estratégia de monetização e sustentabilidade financeira do **Smart Launcher Legend Online (Bacon Knight Launcher)** utilizando a infraestrutura do **AbacatePay**.

O foco principal desta estratégia é garantir:
- **Anonimato do Desenvolvedor:** Manter o nome civil e dados pessoais ocultos dos doadores, exibindo publicamente apenas a marca **Bacon Knight**.
- **Alta Taxa de Conversão:** Oferecer métodos simples e diretos via **PIX instantâneo**.
- **Diversificação de Receita:** Combinar **doações voluntárias por tiers** com **planos de suporte VIP**.

---

## 🛡️ 2. Garantia de Anonimato

Ao utilizar o **AbacatePay**:
1. O pagador visualiza no checkout e no extrato bancário apenas o nome do produto/marca (**Bacon Knight Launcher**) e a intermediadora de pagamento.
2. O e-mail público de suporte vinculado às campanhas utiliza o alias institucional: `contact@baconknight.dev` ou e-mail de criador.
3. Não há exibição de CPF ou nome civil nas telas de pagamento.

---

## 💵 3. Estrutura de Tiers de Doação e Cobrança

Como o AbacatePay trabalha com produtos/links de cobrança, a estratégia é disponibilizar **Tiers de Apoio Predefinidos** que atendem desde doações simbólicas até apoiadores recorrentes:

| Tier de Apoio | Valor | Público-Alvo | Benefício / Reconhecimento |
| :--- | :---: | :--- | :--- |
| ☕ **Café do Dev** | **R$ 5,00** | Jogadores casuais | Agradecimento na Landing Page / Discord |
| 🛡️ **Apoiador Bronze** | **R$ 15,00** | Jogadores ativos | Cargo exclusivo "Apoiador" no Discord |
| ⚔️ **Apoiador Prata** | **R$ 30,00** | Multi-boxers | Cargo "VIP Supporter" + Acesso antecipado a atualizações |
| 👑 **Patrono Ouro** | **R$ 50,00+** | Guildas e Líderes | Cargo "Patrono" + Suporte prioritário para macros customizadas |

---

## 🏗️ 4. Fluxo de Integração Técnica

### A. Landing Page (`docs/index.html`)
- **Seção de Doação Redesenhada:** Substituição de links antigos por um Grid de Tiers com botões diretos de checkout do AbacatePay.
- **QR Code Dinâmico:** Geração de checkout responsivo compatível com dispositivos móveis e desktop.

### B. Aplicativo Launcher (`src/ui/`)
- **Pop-up de Agradecimento e Apoio:**
  - Janela modal amigável com os botões de doação direta.
  - Ao clicar no tier desejado, abre o navegador padrão no checkout seguro do AbacatePay.

---

## 🚀 5. Roteiro de Execução (Roadmap de Implementação)

1. **Fase 1: Configuração no AbacatePay**
   - [x] Ajuste de anonimato e sanitização de dados no projeto (concluído).
   - [ ] Cadastro da conta de criador no [AbacatePay](https://abacatepay.com).
   - [ ] Criação dos 4 produtos/links de cobrança (R$ 5, R$ 15, R$ 30 e R$ 50).

2. **Fase 2: Atualização da Web e do App**
   - [ ] Atualizar os links de doação na Landing Page ([`docs/index.html`](file:///c:/Users/mariano/Documents/Launcher/docs/index.html)).
   - [ ] Atualizar o modal de doação dentro do Launcher ([`src/ui/launcher_hub.py`](file:///c:/Users/mariano/Documents/Launcher/src/ui/launcher_hub.py)).

3. **Fase 3: Engajamento da Comunidade**
   - [ ] Divulgar os canais de apoio no servidor do Discord oficial.
   - [ ] Automatizar cargos no Discord via webhook de confirmação (opcional).

---

*Documento mantido pela equipe de desenvolvimento Bacon Knight.*
