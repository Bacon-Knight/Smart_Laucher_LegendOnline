<div align="center">
  <img src="https://via.placeholder.com/150/482963/FFFFFF?text=Legend+Launcher" alt="Logo" width="120" />
  <h1>Legend Online - Custom Launcher Otimizado</h1>
  <p><strong>Desenvolvido com Foco Extremo em Performance, Multi-Boxing e Macros Background</strong></p>
</div>

---

O **Legend Online Custom Launcher** foi desenvolvido com o propósito de substituir ferramentas desatualizadas e permitir o acesso definitivo e sem bugs ao jogo em 2026+. Ele é construído em cima de **Python 3** e do motor C++ do **Chromium** embedado via PyQt5, trazendo consigo o Plugin PPAPI do Adobe Flash Player de forma nativa e segura.

## ✨ Por que este Launcher? (Diferenciais)

- **UI Gamer (Frameless):** Interface limpa sem as bordas quadradas padrões do sistema. Janela totalmente arrastável, redimensionável (pelas extremidades) e com tema customizado (Roxo/Preto/Dourado).
- **Multi-Sessões Isoladas (Multi-Boxing):** Você pode jogar com dezenas de contas ao mesmo tempo. Cada "Janela de Jogo" possui um *Profile Chromium Independente*, impedindo que o cookie de login de uma deslogue a outra.
- **Gerenciamento de Contas Inteligente:** O "Hub" inicial permite o preenchimento automático. Ele salva e gerencia E-mail, Senha, Servidor e o seu Nickname. Você pode acessar sua lista visual com 1 clique.
- **Injeção Automática de Login:** Não quer ficar digitando? Ele lê os campos do Hub, carrega o site e manda pacotes de JavaScript injetados direto no DOM para fazer login automático por você!
- **Auto-Zoom Matemático:** O jogo redimensiona os gráficos sem cortá-los. Divida sua tela em 4 ou mais janelinhas, e o zoom acompanha o tamanho perfeitamente, garantindo visão 100%.

## 🤖 Sistema de Macros Embutido (Invisível)

A verdadeira genialidade deste Launcher está no fato de ele não usar o "mouse do sistema operacional" para enviar macros. As Macros disparam pacotes diretamente para a renderização interna da página. Isso significa que **os macros funcionam com o jogo minimizado**!

1. **AutoClicker Fantasma (F4):** Deixe farmando dezenas de instâncias num local da tela. A cada 1s o motor clica no X/Y predefinido de forma invisível.
2. **Formação Mágica (Macro 5x5):** Um mini-robô autônomo baseado em Geometria Isométrica. Com 1 clique no centro de um tabuleiro, ele mapeia 25 pontos e dispara golpes cadenciados (respeitando o delay de combate de X segundos que você escolhe) na sequência exata de vitória.

## 🛠️ Ferramentas & Guias In-Game
O Launcher possui um pequeno botão de Ferramentas (`🛠`) na borda da janela. Nele, você pode acessar:
- Suas bibliotecas de **Planos de Crise** (Galerias de imagens que abrem flutuantes na tela para te ajudar nas dungeons).
- Plantas completas das **Minas** do Jogo (Atual, Baixo/Médio, Grande).
- Botões Rápidos para Limpar Cache de Memória e Mutar aba (útil para multi-boxing).

---

## 🧠 Nova Arquitetura Modular (v2.0)

O projeto foi completamente refatorado e separado em módulos dentro da pasta `src/` para facilitar a manutenção e escalabilidade:
- **`src/core/`**: Gerenciamento de macros via `QThread` (rodando em paralelo sem travar a UI), sistema central de configurações e gerador de logs (`logger.py`). O cache e os logs de erros agora são salvos de forma limpa na pasta oficial `%LOCALAPPDATA%\\LegendOnlineLauncher`.
- **`src/ui/`**: A interface e seus componentes. Conta com uma classe base inteligente (`FramelessWindowMixin`) que garante sombras, cantos arredondados e ativa o recurso *Snap Layouts* (Auto-Tile) de forma nativa no Windows!

## 💻 Instalação & Compilação
Se você é um jogador final, basta baixar o executável e colocar na mesma pasta do seu `pepflashplayer.dll`.

Se você for modificar o código:
### Requisitos
- Python 3.x
- Pacotes instalados: `pip install PyQt5 PyQtWebEngine pyinstaller`
- O arquivo nativo `pepflashplayer.dll` na raiz do projeto (versão PPAPI 32.0.0.371)
- O arquivo `style.qss` customizado

### Como compilar para `.exe` portátil
```bash
pyinstaller --noconsole --onefile --add-data "style.qss;." launcher.py
```

## 🧠 Para Inteligências Artificiais e IDEs (Copilot, Cursor)
O contexto de arquitetura para auxílio de código (LLMs) está externalizado. Leia urgentemente o arquivo:
👉 `docs/AI_CONTEXT.md`

Para ver o rumo que estamos tomando (Roadmap, Ubuntu):
👉 `docs/ROADMAP.md`