# 🚀 Legend Online Launcher — Release Notes v2.3

## 🌟 O que há de novo na Versão 2.3

### ⚔️ Automação de Auto-Luta de Combate (Atalho F5)
- **Modo Combate em Segundo Plano**: Rotaciona ciclicamente as habilidades (`1, 2, 3, 4, 5`), runas (`Q, W, E`) e ativação de Sylph / Despertar (`Espaço`).
- **Livre do Mouse e Teclado do SO**: Os comandos de entrada são postados diretamente para o motor gráfico da janela sem sequestrar o cursor ou teclado do Windows.
- **Painel Flutuante e Menu**: Botão rápido **`⚔️ Auto-Luta (F5): OFF / ON`** integrado ao painel flutuante de macros (`⚡`) e menu de ferramentas (`🛠`).

### ⏰ Correções e Ajustes no Agendamento Pré-Evento
- **Inteligência de Agendamento**: Corrigido o disparo de relogs de rotina que ocorriam ~45 a 60 minutos antes de eventos (como World Boss e CB).
- **Priorização de Eventos**: Quando um aviso pré-evento (15 min antes) ocorrer em até 2h30 (150 min), o agendador prioriza diretamente o evento, evitando popups redundantes.

### 🛡️ Correção da Bandeja (System Tray) e Restauração de Janelas
- **Ocultação Imediata**: Ao fechar uma janela de jogo, o ícone na bandeja do Windows é ocultado instantaneamente (`self.tray_icon.hide()`) e todos os temporizadores ativos são interrompidos.
- **Desregistro no Hub**: Janelas encerradas são desregistradas da lista ativa do controlador do Hub, impedindo a reabertura de quadros pretos ao acionar o Modo Chefe / Exibir Todos.

---

## 📦 Arquivos da Release v2.3
- `LegendOnlineLauncher_v2.3.exe` (Executável Windows Portátil)
- `LegendOnlineLauncher_v2.3.spec` (Arquivo de Build PyInstaller Windows)
- `LegendOnlineLauncher_v2.3_linux.spec` (Arquivo de Build PyInstaller Linux)
