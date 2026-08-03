# 📊 Análise Completa da Arquitetura MVC e Desempenho — Smart Launcher Legend Online

---

## 📌 1. Visão Geral do Projeto

O **Smart Launcher Legend Online** (v2.2) é uma aplicação desktop desenvolvida em **Python 3** utilizando a biblioteca **PyQt5** (com `QWebEngineView`) e o plugin **Pepper Flash (PPAPI)** (`pepflashplayer.dll` / `libpepflashplayer.so`).

O projeto adota o padrão de projeto **MVC (Model-View-Controller)** para desacoplar regras de negócio, dados e visualização de interface.

---

## 🏗️ 2. Arquitetura MVC do Sistema

```
                          +-----------------------+
                          |        main.py        |
                          | (Bootstrap da App)    |
                          +-----------+-----------+
                                      |
                                      v
                          +-----------------------+
                          |     HubController     |  <--->  HubView (UI)
                          | (Contas, AFK, Sessions|
                          +-----------+-----------+
                                      |
                +---------------------+---------------------+
                |                                           |
                v                                           v
     +--------------------+                       +--------------------+
     |   GameController 1 |                       |   GameController 2 |
     | (Auto-Relog / RAM) |                       | (Auto-Relog / RAM) |
     +---------+----------+                       +---------+----------+
               |                                            |
               v                                            v
     +--------------------+                       +--------------------+
     |    GameView 1      |                       |    GameView 2      |
     |  (QtWebEngine UI)  |                       |  (QtWebEngine UI)  |
     +--------------------+                       +--------------------+
```

### Principais Componentes MVC:

1. **Camada MODEL ([`src/models/`](file:///c:/Users/mariano/Documents/Launcher/src/models/))**:
   - `account.py`: Dataclass pura com serialização `to_dict()` e `from_dict()`.
   - `game_session.py`: Dados da sessão de jogo em execução.
   - `relog_schedule.py`: Calculador de horários pré-evento (15 min antes das `11h`, `13h`, `15h`, `17h`, `19h`, `21:35`).

2. **Camada CONTROLLER ([`src/controllers/`](file:///c:/Users/mariano/Documents/Launcher/src/controllers/))**:
   - `hub_controller.py`: Controla operações de salvamento/exclusão de contas, `AFKManager` e disparo de sessões.
   - `game_controller.py`: Controla o ciclo de vida da janela do jogo, agendamento do Auto-Relog, `fast_relog()` (`about:blank` + `gc.collect()`), zoom debounced e macros.

3. **Camada VIEW ([`src/ui/views/`](file:///c:/Users/mariano/Documents/Launcher/src/ui/views/))**:
   - `hub_view.py`: Construção visual do Hub do Launcher em PyQt5.
   - `game_view.py`: Construção visual da Janela do Jogo com a `QWebEngineView`.

4. **Componentes Reutilizáveis de UI ([`src/ui/components/`](file:///c:/Users/mariano/Documents/Launcher/src/ui/components/))**:
   - `dialogs.py`: Inclui o `RelogPromptDialog` com barra de contagem regressiva de 15s.
   - `title_bar.py`: Barra de título customizada frameless.
   - `floating_macro.py`: Painel flutuante de atalhos.
   - `frameless.py`: Mixin para janelas sem bordas e resize nativo.

5. **Infraestrutura Core ([`src/core/`](file:///c:/Users/mariano/Documents/Launcher/src/core/))**:
   - `webengine.py`: Flags do Chromium ativas (`--disable-background-timer-throttling`, `--js-flags=--max-old-space-size=1024`).
   - `logger.py`: Registrador com codificação segura UTF-8 e mascaramento de e-mails.

---

## 🔍 3. Otimizações de Desempenho e Engenharia de Software

1. **Isolamento de Cache de Disco por Conta**:
   - Cada conta tem seu próprio subdiretório de cache em disco, eliminando concorrência de leitura/gravação (*File Locks*) no Windows durante o multi-boxing.

2. **Gerenciamento Inteligente de RAM (Garbage Collection)**:
   - A chamada `fast_relog()` descarrega a página para `about:blank` e força a execução do `gc.collect()`, devolvendo a memória liberada pelo Pepper Flash Player ao sistema operacional.

3. **Injeção de Eventos Qt (`QCoreApplication.postEvent`)**:
   - Automação via mensagens do Qt sem capturar o cursor do mouse do SO, funcionando com o jogo minimizado ou em segundo plano.

---

## 📈 4. Conclusão

A arquitetura **MVC** consolidou o *Smart Launcher Legend Online v2.2* como uma plataforma desacoplada, escalável, extremamente leve e altamente resiliente.
