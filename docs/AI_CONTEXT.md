# Legend Online - Custom Launcher Arquitetura & Contexto

Este documento serve como a **Bíblia de Arquitetura e Contexto** deste projeto. Se você é um LLM (Agente IA, Copilot, Cursor, Gemini, etc.) e está lendo este documento, trate as informações aqui descritas como a fonte primária da verdade sobre como e porquê este software foi construído.

## 1. O Problema Original
O jogo "Legend Online" é um clássico jogo de browser que dependia fortemente do Adobe Flash Player. Com a morte do Flash, a única maneira de jogar era através de launchers de terceiros pesados, mal otimizados e limitados a poucas instâncias.
O objetivo deste projeto foi criar um **Launcher Leve, Escalável e Injetável** que permita o **Multi-Boxing** (jogar com 10, 20 contas simultaneamente no mesmo PC), além de incluir macros indetectáveis.

## 2. Escolha da Stack de Tecnologia
- **Python 3:** Linguagem base, excelente para prototipagem rápida e automações.
- **PyQt5:** O Framework gráfico escolhido no lugar do PyQt6 ou PySide. O motivo principal para isso é que **apenas o motor WebEngine antigo do PyQt5 suporta a injeção nativa do plugin NPAPI/PPAPI do Flash (`pepflashplayer.dll`)**. Tentar migrar este projeto para PyQt6 fará com que o jogo pare de renderizar (tela preta ou de erro do Flash). Não tente atualizar a versão do framework Qt.
- **QWebEngineView:** Um mini-browser Chromium embedado em C++.

## 3. Decisões Arquiteturais e "Hacks" Críticos

### A. O Isolamento de Sessão (Multi-Boxing)
Para que o jogador logue em várias contas sem que o navegador misture os cookies, foi utilizado o `QWebEngineProfile`.
- Cada conta gera um nome de perfil seguro baseado no seu E-mail (`email.replace('@', '_')`).
- Este perfil ganha uma pasta de cache própria local e um `off-the-record profile` (similar à aba anônima persistente) chamado por instâncias separadas.
- **Atenção IA:** Ao alterar a inicialização da `GameWindow`, **NUNCA** faça com que janelas compartilhem o `QWebEngineProfile.defaultProfile()`, ou as contas se cruzarão e deslogarão.

### B. Injeção Auto-Login via JavaScript
Os menus padrão não possuíam API aberta. A solução foi construir um sistema que extrai as informações do `QSettings` da GUI feita no `LauncherHub` e roda um `self.page.runJavaScript()` assim que a página acusa carregamento inicial, injetando login/senha e forçando o `submit()` no formulário de destino.

### C. Sistema de Macros Baseado em Eventos do Qt
Ao invés de utilizar bibliotecas clássicas como `pyautogui`, `keyboard` ou `pynput` que sequestram o mouse real do usuário, este Launcher usa a "Magia Negra" do Qt: `QCoreApplication.postEvent()`.
- O AutoClicker Fantasma pega o alvo X/Y e despacha pacotes puros de `QMouseEvent` direto no ponteiro de `focusProxy()` (o sub-processo de renderização do Chromium).
- O resultado: O usuário pode botar o AutoClick em 3 abas, minimizar todas elas e ir assistir um vídeo no YouTube enquanto o jogo joga sozinho em background.
- **Atenção IA:** Não instale bibliotecas externas de automação GUI. Mantenha os macros via injeção de eventos do Qt.

### D. Formação Mágica (Matemática Isométrica 5x5)
O jogo tem um minigame 5x5 desenhado em perspectiva isométrica. Ao invés de usar processamento de visão pesada (`OpenCV`), descobrimos que o tamanho do grid varia de forma perfeitamente linear baseada no Zoom.
- Base Tile (Zoom 1.0): W=104, H=52
- Calculamos o zoom atual lendo o fator de `resizeEvent`.
- Com um único clique do usuário no centro, mapeamos os 25 pontos através da fórmula:
  ```python
  screen_x = cx + (x - y) * (w / 2)
  screen_y = cy + (x + y) * (h / 2)
  ```
- Executamos os cliques no Background utilizando uma Fila (`QTimer`) respeitando tempos de combate.

### E. Otimizações Extremas do Chromium (Flags)
As flags passadas no `sys.argv` (ver bloco final de `launcher.py`) desativam serviços do Chrome desnecessários (sync, print, rasterization via CPU). Isso corta o uso de memória do WebEngine quase pela metade.

## 4. O Futuro (O que você pode fazer se solicitado)
Leia o arquivo `ROADMAP.md` para entender as integrações pendentes. Use isso para se situar sobre "o que" programar a seguir caso o usuário seja genérico em seu pedido.
