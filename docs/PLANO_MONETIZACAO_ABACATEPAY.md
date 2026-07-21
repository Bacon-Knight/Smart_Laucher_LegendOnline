# ⚡ Plano Estratégico de Monetização e Rentabilidade — Livepix

---

## 📌 1. Visão Geral

Este documento descreve a estratégia de monetização e sustentabilidade financeira do **Smart Launcher Legend Online (Bacon Knight Launcher)** utilizando a infraestrutura do **Livepix**.

O foco principal desta estratégia é garantir:
- **Anonimato do Desenvolvedor (Pessoa Física / CPF):** Receber doações com conta CPF mantendo dados civis ocultos dos doadores, exibindo publicamente apenas a marca **Bacon Knight**.
- **Alta Taxa de Conversão via PIX:** Oferecer doações via QR Code dinâmico e estático com confirmação instantânea.
- **Diversificação de Receita:** Combinar **doações voluntárias por tiers** com **mensagens/alertas de apoiadores**.

---

## 🛡️ 2. Garantia de Anonimato e Segurança (CPF)

Ao utilizar o **Livepix**:
1. O pagador visualiza no checkout do Livepix e no extrato bancário apenas a identificação da intermediadora (**Livepix / PagSeguro**) e o nickname da página (`livepix.gg/baconknight` ou similar).
2. Não há exibição de CPF ou nome civil nas telas de pagamento público.
3. O saque é realizado diretamente para a conta bancária vinculada ao CPF do desenvolvedor sem burocracia de CNPJ.

---

## 💵 3. Estrutura de Tiers de Doação

Com o Livepix, o doador pode inserir o valor desejado ou selecionar os valores predefinidos de apoio:

| Tier de Apoio | Valor | Público-Alvo | Benefício / Reconhecimento |
| :--- | :---: | :--- | :--- |
| ☕ **Café do Dev** | **R$ 5,00** | Jogadores casuais | Agradecimento na Landing Page / Discord |
| 🛡️ **Apoiador Bronze** | **R$ 15,00** | Jogadores ativos | Cargo exclusivo "Apoiador" no Discord |
| ⚔️ **Apoiador Prata** | **R$ 30,00** | Multi-boxers | Cargo "VIP Supporter" + Acesso antecipado a atualizações |
| 👑 **Patrono Ouro** | **R$ 50,00+** | Guildas e Líderes | Cargo "Patrono" + Suporte prioritário para macros customizadas |

---

## 🏗️ 4. Fluxo de Integração Técnica

### A. Landing Page (`docs/index.html`)
- **Widget de QR Code / Link Livepix:** Incorporar o widget oficial ou o botão direto direcionando para o link de apoio do Livepix.
- **QR Code Dinâmico:** Exibição do QR Code de doação diretamente na web.

### B. Aplicativo Launcher (`src/ui/`)
- **Pop-up de Agradecimento e Apoio:**
  - Janela modal amigável com botão direto "Apoiar via PIX (Livepix)".
  - Ao clicar no botão, abre o navegador no checkout do Livepix ou exibe o QR Code no próprio app.

---

## 🚀 5. Roteiro de Execução (Roadmap de Implementação)

1. **Fase 1: Configuração no Livepix**
   - [x] Transição de AbacatePay para Livepix (Conta Pessoa Física/CPF).
   - [x] Link de apoio configurado: [https://livepix.gg/baconknigth](https://livepix.gg/baconknigth).

2. **Fase 2: Atualização da Web e do App**
   - [x] Integrar o botão oficial do Livepix na Landing Page ([`docs/index.html`](file:///c:/Users/mariano/Documents/Launcher/docs/index.html)).
   - [ ] Atualizar as telas e diálogos de apoio dentro do Launcher (`src/ui/components/dialogs.py` e `src/ui/launcher_hub.py`).

3. **Fase 3: Engajamento da Comunidade**
   - [ ] Divulgar o link de apoio do Livepix no servidor do Discord oficial.

---

*Documento mantido pela equipe de desenvolvimento Bacon Knight.*
