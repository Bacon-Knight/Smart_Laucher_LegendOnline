# Legend Online - Custom Launcher Arquitetura & Contexto

Este documento serve como a **Bíblia de Arquitetura e Contexto** deste projeto. Se você é um LLM (Agente IA, Copilot, Cursor, Gemini, Antigravity, etc.) e está lendo este documento, trate as informações aqui descritas como a fonte primária da verdade sobre como e porquê este software foi construído.

---

## 1. O Problema Original
O jogo "Legend Online" é um clássico jogo de browser que dependia fortemente do Adobe Flash Player. Com a descontinuação do Flash nos navegadores convencionais, a única maneira de jogar era através de launchers de terceiros pesados, mal otimizados, instáveis e limitados a poucas instâncias.

O objetivo deste projeto foi criar um **Launcher Leve, Escalável, Seguro e Injetável** que permita o **Multi-Boxing** (jogar com 10, 20+ contas simultaneamente no mesmo PC), além de incluir automações e macros indetectáveis rodando em segundo plano.

---

## 2. Escolha da Stack de Tecnologia
- **Python 3:** Linguagem base para prototipagem rápida, manipulação de eventos e automação.
- **PyQt5:** O Framework gráfico escolhido no lugar do PyQt6 ou PySide6. O motivo principal para isso é que **apenas o motor WebEngine antigo do PyQt5 suporta a injeção nativa do plugin NPAPI/PPAPI do Flash (`pepflashplayer.dll` no Windows / `libpepflashplayer.so` no Linux)**. Tentar migrar este projeto para PyQt6 fará com que o jogo pare de renderizar (tela preta ou erro de plugin). **Não tente atualizar a versão do framework Qt.**
- **QWebEngineView:** Mini-browser Chromium embedado em C++.

---

## 3. Decisões Arquiteturais e "Hacks" Críticos

### A. Estrutura Modular (`src/`)
- **Ponto de Entrada:** `src/main.py` ➔ Inicializador direto do aplicativo e da interface.
- **`src/main.py`**: Configuração global do `QApplication` e chamada do ambiente Qt WebEngine.
- **`src/core/webengine.py`**: Centralizador dos argumentos de runtime do Chromium/V8 e ativação do plugin Flash.
- **`src/models/account.py`**: Dataclass `Account` encapsulando e-mail, senha, servidor, nickname e cor.
- **`src/services/account_service.py`**: Serviço isolado de CRUD e salvamento/leitura de contas em `QSettings`.
- **`src/assets/js/login.js`**: Script de automação de login sanitizado injetado via WebEngine.
- **`src/ui/launcher_hub.py`**: Hub de gerenciamento de contas, formulário, grade de cartões, Boss Key e notificação pós-crash.
- **`src/ui/game_window.py`**: Janela isolada de execução do jogo, isolamento de perfil, redimensionamento proporcional e atalhos.
- **`src/core/macros.py`**: Motor de macros (`MacroWorker`) rodando em `QThread` paralela.
- **`src/core/logger.py`**: Sistema centralizado de logs, anonimização de dados e relatórios de erros não tratados.


### B. Isolamento de Sessão (Multi-Boxing)
Para que o jogador logue em várias contas sem que o navegador misture os cookies:
- Cada conta gera um nome de perfil seguro baseado em seu e-mail (`safe_email`).
- O `QWebEngineProfile` define `PersistentStoragePath` isolado por conta, garantindo cookies únicos.
- O cache de mídias/assets (SWF, imagens) usa `setCachePath(shared_cache_dir)` compartilhado para economizar banda de rede e acelerar carregamentos.
- **Atenção IA:** Ao alterar a inicialização da `GameWindow`, **NUNCA** faça com que janelas compartilhem o `QWebEngineProfile.defaultProfile()`, ou as contas se cruzarão e deslogarão.

### C. Injeção Auto-Login via JavaScript
Os menus padrão do jogo não possuem API aberta. A solução extrai credenciais sanitizadas via JSON (`LOGIN_JS_SCRIPT`) e executa `self.page.runJavaScript()`, preenchendo os campos do DOM e submetendo o formulário automaticamente no evento `loadFinished`.

### D. Sistema de Macros Baseado em Eventos do Qt (Background)
O Launcher não utiliza bibliotecas de automação baseadas no SO (como `pyautogui` ou `pynput`).
- Os cliques e teclas são despachados diretamente ao widget de renderização do Chromium (`focusProxy()`) via `QCoreApplication.postEvent()`.
- **Resultado:** O usuário pode rodar macros em múltiplas janelas minimizadas sem perder o controle do mouse do sistema operacional.

### E. Formação Mágica (Matemática Isométrica 5x5)
Mapeamento geométrico linear baseado no zoom da janela. A partir de um ponto central e das dimensões dos tiles escalados pelo zoom, gera-se uma fila de coordenadas para 25 posições disparadas via `QTimer`.

### F. Visão Computacional Leve (`check_autoluta`)
Para a funcionalidade de Auto-Luta (F5), o leitor de tela lê pixels específicos para identificar o orbe de combate.
- **Otimização Crítica:** O `grab()` do navegador utiliza uma sub-região recortada (`crop_rect = QRect(...)`) focada apenas na área do HUD, evitando alocar imagens completas da janela a cada 2 segundos.

### G. Gerenciamento de Memória, Flags do Chromium & Performance
- **Heap V8 Expandido (`--js-flags=--max-old-space-size=2048`):** Impede que a engine JavaScript entre em Garbage Collection Thrashing contínuo (causa do lag após 15 minutos).
- **Aceleração por Hardware (`--enable-gpu-compositing`):** Habilita composição de camadas por GPU.
- **Serviços de Fundo Desativados:** Flags como `--disable-background-networking`, `--disable-sync`, `--disable-component-update` cortam tarefas ociosas do Chromium.
- **Throttling no `eventFilter`:** A redefinição do `idle_timer` durante o movimento do mouse é limitada a 1 vez a cada 10 segundos.
- **Garbage Collection no Fast Relog:** `fast_relog()` descarrega a página para `about:blank` e força `gc.collect()`.
- **Limpeza de Threads (`PingWorker`):** Threads de ping conectam `.finished.connect(self.ping_worker.deleteLater)` para desalocar memória.
- **Destruição Segura de Objetos Qt:** `closeEvent` e `resizeEvent` protegem chamadas ao `QWebEnginePage` usando a flag `_is_closing` e tratamento defensivo contra `RuntimeError`.

### H. Diagnóstico, Erros e Notificação de Crashes
- **Códigos de Erro Estruturados:** `setup_global_exception_handler()` em `logger.py` classifica exceções em códigos (`ERR-QT-501`, `ERR-NET-400`, `ERR-MEM-500`, `ERR-REF-404`, `ERR-UNK-999`).
- **Relatório Pós-Crash:** Se a aplicação cair, `QSettings` armazena o evento e `check_previous_crash()` no `LauncherHub` exibe uma janela informativa com o botão **"📁 Abrir Pasta do Log"**.
- **Privacidade (`mask_email`):** Todos os e-mails registrados no log são anonimizados (ex: `e******1@gmail.com`). Senhas jamais são gravadas.

---

## 4. O Futuro e Roadmap
Consulte o arquivo `docs/ROADMAP.md` para verificar pendências e próximas funcionalidades planejadas.
