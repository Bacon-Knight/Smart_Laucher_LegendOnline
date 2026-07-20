<div align="center">
  <img src="docs/assets/logo.png" alt="Logo Bacon Knight" width="150" />
  <h1>Legend Online - Bacon Knight Launcher</h1>
  <p><strong>Desenvolvido com Foco Extremo em Performance, Multi-Boxing, Otimização de Memória e Macros Background</strong></p>
</div>

---

O **Legend Online Custom Launcher** foi desenvolvido com o propósito de substituir ferramentas desatualizadas e permitir o acesso definitivo e sem bugs ao jogo em 2026+. Ele é construído em cima de **Python 3** e do motor C++ do **Chromium** embedado via PyQt5, trazendo consigo o Plugin PPAPI do Adobe Flash Player de forma nativa, segura e de alto desempenho.

## ✨ Por que este Launcher? (Diferenciais)

- **UI Gamer (Frameless):** Interface limpa sem as bordas quadradas padrões do sistema. Janela totalmente arrastável, redimensionável (pelas extremidades) e com tema customizado (Roxo/Preto/Dourado).
- **Multi-Sessões Isoladas (Multi-Boxing):** Você pode jogar com dezenas de contas ao mesmo tempo. Cada "Janela de Jogo" possui um *Profile Chromium Independente*, impedindo que o cookie de login de uma deslogue a outra.
- **Otimização Extrema de Desempenho (Zero Lag):** Motor Chromium configurado com 2048 MB de Heap JS V8 (sem o lag de 15 minutos), aceleração gráfica por GPU ativada (`--enable-gpu-compositing`) e desativação de processos pesados em segundo plano.
- **Gerenciamento de Contas Inteligente:** O Hub inicial oferece formulário rápido e grade visual de cartões de conta. Salva e gerencia E-mail, Senha, Servidor e Nickname com atalhos de 1 clique.
- **Injeção Automática de Login:** Lê as credenciais salvas, carrega a página do servidor e envia pacotes de JavaScript sanitizados diretamente no DOM para login automático sem esforço.
- **Auto-Zoom Matemático:** O jogo redimensiona os gráficos proporcionalmente sem cortá-los, garantindo visão 100% em qualquer resolução ou layout de tela dividida.
- **Privacidade e Logs Seguros:** Anonimização automática de e-mails em logs de diagnóstico e recuperação automática de erros não tratados.

## 🤖 Sistema de Macros Embutido (Invisível & Background)

A automação não utiliza o ponteiro físico do mouse do sistema operacional. As macros disparam pacotes diretamente para a renderização interna da página via `QCoreApplication.postEvent`. **Os macros funcionam com o jogo minimizado!**

1. **AutoClicker Fantasma (F4):** Clique contínuo em coordenadas específicas em segundo plano.
2. **Formação Mágica (Macro 5x5):** Robô autônomo baseado em Geometria Isométrica. Mapeia 25 pontos do tabuleiro a partir do centro e dispara ataques cadenciados.
3. **Gravador de Macro Customizável (F7/F8):** Gravação em tempo real de cliques e teclas com precisão milimétrica de atrasos. Reprodução por F8 e parada instantânea por F4.
4. **Auto-Luta Inteligente (F5):** Algoritmo de visão computacional otimizado que analisa recortes leves (`QRect`) da barra de combate para engajar automaticamente em batalhas.

## 🛡️ Diagnóstico, Erros e Notificação de Crashes

O Launcher conta com um sistema avançado de resiliência e diagnóstico:
- **Códigos de Erro Estruturados:** Erros são categorizados em códigos padrão (ex: `ERR-QT-501` para liberação de componentes Qt, `ERR-NET-400` para rede, `ERR-MEM-500` para estouro de memória).
- **Relatório de Crash ao Reabrir:** Se a aplicação for interrompida por uma exceção não tratada, ao reabrir o Launcher uma janela informativa é exibida com o código do erro, o caminho do arquivo de log e o botão **"📁 Abrir Pasta do Log"**.
- **Logs Anônimos e Seguros:** E-mails de usuários são mascarados nos arquivos de log (ex: `e******1@gmail.com`) e senhas nunca são registradas em disco.

## 🕵️‍♂️ Modo Furtivo & Stealth
- **Minimização Stealth:** Ao pressionar `Ctrl+Shift+A` ou após inatividade prolongada, a janela do jogo e o Hub desaparecem da barra de tarefas e passam a rodar silenciosamente na bandeja do sistema (*System Tray*).

## 🛠️ Ferramentas In-Game
Pelo menu de ferramentas (`🛠`) na barra de título da janela do jogo, é possível acessar:
- Galerias flutuantes de **Planos de Crise** e **Plantas das Minas** (Atual, Baixo/Médio, Grande).
- **Fast Relog (🔄 / 🧹):** Descarregamento e limpeza instantânea da memória RAM com acionamento do Garbage Collector em menos de 1 segundo.
- Indicador de **Ping em Tempo Real** do servidor.

---

## 🧠 Arquitetura do Projeto

A base de código está organizada sob o diretório `src/`:
- **`src/core/`**: Gerenciador de macros em threads secundárias (`macros.py`), configurações e caminhos globais (`config.py`), e registrador central de logs com segurança e captura de erros (`logger.py`).
- **`src/ui/`**: Hub do Launcher (`launcher_hub.py`), janelas de jogo isoladas (`game_window.py`), componentes visuais (`title_bar.py`, `frameless.py`, `dialogs.py`) e painel flutuante de macros (`floating_macro.py`).

Os arquivos de log e cache persistem em `%LOCALAPPDATA%\LegendOnlineLauncher`.

## 💻 Instalação e Compilação

### Requisitos de Desenvolvimento
- Python 3.x
- Dependências: `pip install PyQt5 PyQtWebEngine pyinstaller pillow`
- Arquivo PPAPI Flash `pepflashplayer.dll` na raiz do projeto (Windows) ou `libpepflashplayer.so` (Linux).

### Compilação Standalone (`.exe`)
```bash
pyinstaller --noconsole --onefile --icon="bacon_knight.ico" --add-data "style.qss;." --add-data "pepflashplayer.dll;." --add-data "Ferramentas;Ferramentas" --add-data "bacon_knight.ico;." --name "LegendOnlineLauncher_v2.1" launcher.py
```

## 📚 Documentação Complementar
- 👉 Contexto e decisões para IAs/LLMs: `docs/AI_CONTEXT.md`
- 👉 Análise detalhada da arquitetura: `docs/ANALISE_DO_PROJETO.md`
- 👉 Manual de instruções do usuário final: `docs/MANUAL_DE_USO.md`
- 👉 Plano de desenvolvimento e futuro: `docs/ROADMAP.md`