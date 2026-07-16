<div align="center">
  <img src="docs/assets/logo.png" alt="Logo Bacon Knight" width="150" />
  <h1>Legend Online - Bacon Knight Launcher</h1>
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
2. **Formação Mágica (Macro 5x5):** Um mini-robô autônomo baseado em Geometria Isométrica. Com 1 clique no centro de um tabuleiro, ele mapeia 25 pontos e dispara golpes cadenciados.
3. **Gravador de Macro Customizável (F7/F8):** Você pode gravar seus próprios cliques e teclas do teclado em tempo real apertando F7. Ele salva os atrasos (delays) milimetricamente e você dá play na automação apertando F8. Funciona com a janela minimizada!
4. **Auto-Luta (F5):** Um algoritmo de visão computacional varre pixels específicos na tela para detectar botões laranjas/vermelhos e engaja no combate automaticamente.

## 🕵️‍♂️ Modo Furtivo & Privacidade Total
O Launcher foi pensado para você jogar onde quiser com privacidade:
- **Minimização Stealth:** Ao minimizar a tela (ou apertar `Ctrl+Shift+A`, ou passar 90 segundos sem tocar no mouse), a janela do jogo DESAPARECE completamente da Barra de Tarefas e vai parar em formato minúsculo silenciado lá no *System Tray* (bandeja do relógio do Windows), rodando com o icone do Bacon Knight. Ninguém vai ver que o jogo está aberto.

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
Se você é um jogador final, basta baixar **ÚNICO executável** gerado. Diferente das versões antigas, o `pepflashplayer.dll` agora é embutido diretamente dentro do EXE, tornando-o um sistema *Standalone* Portátil!

Se você for modificar o código:
### Requisitos
- Python 3.x
- Pacotes instalados: `pip install PyQt5 PyQtWebEngine pyinstaller pillow`
- O arquivo nativo `pepflashplayer.dll` na raiz do projeto (versão PPAPI 32.0.0.371)
- O ícone customizado `bacon_knight.ico`

### Como compilar para `.exe` Standalone (Tudo em Um)
```bash
pyinstaller --noconsole --onefile --icon="bacon_knight.ico" --add-data "style.qss;." --add-data "pepflashplayer.dll;." --name "LegendOnlineLauncher_v2.1" launcher.py
```

## 🧠 Para Inteligências Artificiais e IDEs (Copilot, Cursor)
O contexto de arquitetura para auxílio de código (LLMs) está externalizado. Leia urgentemente o arquivo:
👉 `docs/AI_CONTEXT.md`

Para ver o rumo que estamos tomando (Roadmap, Ubuntu):
👉 `docs/ROADMAP.md`