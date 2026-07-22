<div align="center">
  <img src="docs/assets/logo.png" alt="Logo Bacon Knight" width="150" />
  <h1>Legend Online - Bacon Knight Launcher</h1>
  <p><strong>Desenvolvido em Arquitetura MVC com Foco Extremo em Performance Multi-Boxing, Otimização de RAM e Auto-Relog Inteligente</strong></p>
</div>

---

O **Legend Online Custom Launcher (v2.2)** foi desenvolvido para fornecer o acesso definitivo, sem bugs e de altíssimo desempenho ao jogo. Construído em **Python 3** sobre a arquitetura **MVC (Model-View-Controller)** com motor C++ do **Chromium** embedado via PyQt5, trazendo consigo o Plugin PPAPI do Adobe Flash Player de forma nativa e acelerada por hardware GPU.

## ✨ Por que este Launcher? (Diferenciais da v2.2)

- **Arquitetura MVC Modular:** Separação completa entre Dados/Regras (`models/`), Controladores de Aplicação (`controllers/`) e Interfaces Gráficas (`ui/views/`).
- **Multi-Boxing com Cache Isolado (Zero Travamentos):** Jogue com dezenas de contas simultâneas. Cada conta possui seu perfil e diretório de cache de disco totalmente isolados, eliminando colisões de arquivo (*file locks*) no Windows.
- **Auto-Relog Inteligente Pré-Eventos:**
  - **Proteção de Horários de Eventos:** Impede desconexões durante os eventos principais (`11:00`, `13:00`, `15:00`, `17:00`, `19:00` e `21:35`).
  - **Disparo Preventivo de 15 Minutos:** Executa a reciclagem de memória **15 minutos antes** dos eventos (`10:45`, `12:45`, `14:45`, `16:45`, `18:45` e `21:20`), garantindo o jogo com RAM zerada na hora da batalha.
  - **Aviso com Contagem Regressiva de 15s (`RelogPromptDialog`):** Exibe um diálogo flutuante informando o motivo do relog com as opções: **[ ▶ Relogar Agora ]**, **[ ⏰ Adiar +30 min ]** e **[ ✕ Cancelar ]**. Se o jogador estiver AFK, o relog é concluído automaticamente.
- **Otimização Extrema de RAM e GPU:** Flags do Chromium ajustadas (`--disable-background-timer-throttling`, `--js-flags=--max-old-space-size=1024`) para evitar congelamentos ao alternar entre janelas em segundo plano.
- **Auto-Zoom com Debounce:** Redimensionamento suave sem travamentos durante o arraste das janelas.
- **Gerenciamento de Contas Inteligente:** Hub inicial com formulário rápido, grade visual de cartões de conta e injeção automática de login sanitizado via JavaScript.
- **Inatividade Furtiva & AFK Manager:** Modo Chefe (`Ctrl+Shift+A`) e ocultamento automático para a bandeja do sistema (*System Tray*).

---

## 🤖 Sistema de Macros Embutido (Invisível & Background)

A automação dispara pacotes diretamente para o motor gráfico da página via `QCoreApplication.postEvent`. **Os macros funcionam com o jogo minimizado sem sequestrar o mouse do SO!**

1. **AutoClicker Fantasma (F4):** Clique contínuo em coordenadas específicas em segundo plano.
2. **Formação Mágica (Macro 5x5):** Mapeia 25 pontos do tabuleiro isométrico a partir do centro e dispara ataques cadenciados.
3. **Gravador de Macro Customizável (F7/F8):** Gravação em tempo real de cliques e teclas com precisão milimétrica de atrasos. Reprodução por F8 e parada instantânea por F4.

---

## 🛠️ Ferramentas In-Game

Pelo menu de ferramentas (`🛠`) na barra de título ou pelo painel flutuante (`⚡`), é possível acessar:
- Galerias de **Planos de Crise** e **Plantas das Minas** (Atual, Baixo/Médio, Grande).
- **Fast Relog (🔄 / 🧹):** Descarregamento da aba para `about:blank` com acionamento do *Garbage Collector* para liberar a RAM do Flash Player em menos de 1 segundo.

---

## 🧠 Arquitetura do Projeto (MVC)

A base de código está organizada sob o diretório `src/`:
- **`src/models/`**: Modelos de dados e regras de negócio (`account.py`, `game_session.py`, `relog_schedule.py`).
- **`src/controllers/`**: Controladores que coordenam as regras da aplicação (`hub_controller.py`, `game_controller.py`).
- **`src/ui/views/`**: Telas de interface gráfica desacopladas (`hub_view.py`, `game_view.py`).
- **`src/ui/components/`**: Componentes reutilizáveis de UI (`title_bar.py`, `dialogs.py`, `floating_macro.py`, `frameless.py`).
- **`src/services/`**: Serviços desacoplados de persistência em `QSettings` (`account_service.py`).
- **`src/core/`**: Utilitários do sistema, loggers e WebEngine (`webengine.py`, `logger.py`, `macros.py`, `config.py`).
- **`src/main.py`**: Ponto de entrada e bootstrap da aplicação.

---

## 💻 Instalação e Compilação

### 🪟 1. Execução no Windows
1. Acesse as [Releases Oficiais no GitHub](https://github.com/Bacon-Knight/Smart_Laucher_LegendOnline/releases/latest).
2. Baixe o executável **`LegendOnlineLauncher_v2.2.exe`**.
3. Execute diretamente com dois cliques (não requer instalação prévia).

---

### 🐧 2. Compilação e Instalação no Ubuntu / Linux (Na Própria Máquina)

#### 📋 Passo 1: Instalar as Dependências do Sistema
```bash
sudo apt update
sudo apt install python3 python3-pip python3-pyqt5 python3-pyqt5.qtwebengine
pip install pyinstaller pillow
```

#### 🛠️ Passo 2: Clonar o Repositório e Executar o Script Automático
```bash
git clone https://github.com/Bacon-Knight/Smart_Laucher_LegendOnline.git
cd Smart_Laucher_LegendOnline
chmod +x build_fixed.sh
./build_fixed.sh
```

#### 📦 Passo 3: Instalar o pacote `.deb` ou rodar o `AppImage`
```bash
# Instalar o pacote Debian/Ubuntu:
sudo dpkg -i legend-online-launcher_2.2.0_amd64.deb

# Ou executar o AppImage portátil:
chmod +x Legend-Online-Launcher-v2.2-x86_64.AppImage
./Legend-Online-Launcher-v2.2-x86_64.AppImage
```

---

### 🛠️ 3. Compilação Manual no Windows (`.exe`)
```bash
python -m PyInstaller --noconfirm LegendOnlineLauncher_v2.2.spec
```

---

## 📚 Documentação Complementar
- 👉 **Manual de Instruções do Usuário Final:** [`docs/MANUAL_DE_USO.md`](file:///c:/Users/mariano/Documents/Launcher/docs/MANUAL_DE_USO.md)
- 👉 **Análise Técnica da Arquitetura:** [`docs/ANALISE_DO_PROJETO.md`](file:///c:/Users/mariano/Documents/Launcher/docs/ANALISE_DO_PROJETO.md)
- 👉 **Landing Page Oficial:** [`docs/index.html`](file:///c:/Users/mariano/Documents/Launcher/docs/index.html)
- ⚡ **Apoiar o Desenvolvedor:** [Livepix (PIX)](https://livepix.gg/baconknigth)