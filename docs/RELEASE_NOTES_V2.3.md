# 🥓 Bacon Knight Launcher v2.3

O **Bacon Knight Launcher v2.3** é a versão definitiva para jogar Legend Online com alta performance, suporte a dezenas de contas simultâneas (Multi-Boxing), Auto-Luta (F5) e navegação segura com Flash PPAPI embutido no Windows e no Ubuntu/Linux.

Nesta atualização, trouxemos a nova automação de **Auto-Luta de Combate (F5)**, correções inteligentes nos horários de avisos de relog pré-evento, resolução do ícone retido na bandeja (System Tray) e limpeza de janelas pretas ao restaurar o Hub.

---

## ✨ Principais Novidades & Recursos

* ⚔️ **Auto-Luta de Combate Automática (F5)**: Rotaciona ciclicamente as habilidades (`1, 2, 3, 4, 5`), runas (`Q, W, E`) e ativação de Sylph (`Espaço`) 100% em segundo plano, enviando os comandos para o motor gráfico sem sequestrar o mouse ou teclado do SO.
* ⏰ **Agendamento Inteligente Pré-Eventos**: Corrigido o disparo de relogs de rotina redundantes que ocorriam ~45 a 60 minutos antes de eventos principais (World Boss e CB). Se o evento ocorrer em até 2h30, o sistema prioriza diretamente o pré-evento (15 min antes).
* 🛡️ **Correção da Bandeja & Restauração Furtiva**: Ao fechar o jogo, o ícone do Javali desparece instantaneamente da bandeja do Windows (System Tray), e o Hub desregistra instâncias encerradas, impedindo telas pretas residuais ao acionar o Modo Chefe (`Ctrl+Shift+A`).
* ⚡ **Desempenho Otimizado do Flash**: Melhorias no ciclo de inicialização do motor Chromium e plugins do Flash PPAPI, eliminando lags de travamento.
* 👥 **Multi-Boxing Isolado**: Cada conta possui um perfil isolado de navegação. Jogue com dezenas de contas ao mesmo tempo sem conflitos de login.
* 👻 **Macros Background Invisíveis**: Macros de AutoClicker, Formação Mágica 5x5 e Auto-Luta operam em segundo plano diretamente no renderizador, mesmo com o jogo minimizado.
* 🥷 **Modo Stealth (Furtivo)**: Atalho `Ctrl+Shift+A` esconde instantaneamente todas as janelas do Launcher na bandeja do sistema (System Tray).
* 🚀 **Automação de Login no Hub**: Cadastre suas contas e entre no jogo com apenas 1 clique.
* 💳 **Apoio ao Projeto (Livepix)**: Canal oficial de doações instantâneas via PIX com total privacidade para o criador e apoiadores.

---

## 💾 Download e Guia de Instalação

### 🪟 1. Instalação no Windows (Executável Pronto)

1. Faça o download do arquivo executável: **`LegendOnlineLauncher_v2.3.exe`** (anexado abaixo nos Assets da Release).
2. Não é necessário instalar: basta dar dois cliques sobre o arquivo `LegendOnlineLauncher_v2.3.exe` para iniciar o Launcher.
3. *(Opcional)* Crie um atalho na sua Área de Trabalho para acesso rápido.

---

### 🐧 2. Compilação e Execução no Ubuntu / Linux (Na Própria Máquina)

Para rodar o Launcher no Ubuntu ou qualquer distribuição baseada em Debian/Linux compilando na sua própria máquina, siga os passos abaixo:

#### 📋 Passo 1: Instalar as Dependências do Sistema

Abra o terminal e instale o Python 3 e os módulos necessários:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-pyqt5 python3-pyqt5.qtwebengine
pip install pyinstaller pillow
```

#### 🛠️ Passo 2: Baixar o Código e Executar a Compilação Automática

Baixe o código-fonte desta release (`Source code.zip` / `Source code.tar.gz`) ou clone o repositório:

```bash
git clone https://github.com/Bacon-Knight/Smart_Laucher_LegendOnline.git
cd Smart_Laucher_LegendOnline
```

Dê permissão de execução e rode o script automatizado de compilação:

```bash
chmod +x build_fixed.sh
./build_fixed.sh
```

O script criará automaticamente na sua máquina:
- O executável de Linux em `dist/LegendOnlineLauncher_v2.3_linux`
- O pacote de instalação `.deb`: `legend-online-launcher_2.3.0_amd64.deb`
- O pacote portátil AppImage: `Legend-Online-Launcher-v2.3-x86_64.AppImage`

#### 🚀 Passo 3: Instalar o pacote .deb gerado

Após rodar o script, você pode instalar o pacote `.deb` gerado com:

```bash
sudo dpkg -i legend-online-launcher_2.3.0_amd64.deb
```

E iniciar o jogo pelo menu de aplicativos ou pelo comando `legend-launcher`.

---

## 💬 Comunidade & Suporte

- 💬 **Discord Oficial**: Junte-se à nossa comunidade
- ⚡ **Apoiar o Desenvolvedor**: Doe via PIX no Livepix

*Bacon Knight Launcher — Software independente desenvolvido para a comunidade de Legend Online.*
