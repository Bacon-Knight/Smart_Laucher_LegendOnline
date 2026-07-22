# 📖 Manual de Uso - Bacon Knight Launcher (v2.2)

Bem-vindo ao manual oficial do **Bacon Knight Launcher (v2.2)**. Aqui você vai aprender a tirar o máximo de proveito da nova arquitetura MVC, sistema de multi-boxing, Auto-Relog Inteligente, otimizações de performance e stealth.

---

## 🚀 1. Primeiros Passos e Login
1. Ao abrir o aplicativo, você verá o **Hub de Contas** com formulário e cartões visuais.
2. Preencha seus dados de acesso (E-mail e Senha) e escolha o Servidor.
3. (Opcional) Digite um apelido/nick para organizar suas contas (ex: "Arqueiro Principal").
4. Clique em **" INICIAR JOGO "**. O Launcher salvará a conta na grade visual e fará o login automático!
5. Para jogar com contas salvas anteriormente, basta clicar em **"▶ Entrar"** no cartão da conta na grade.

---

## ⚡ 2. O Poder do Multi-Boxing com Cache Isolado
Ao contrário de navegadores normais que misturam cookies ou desconectam contas simultâneas, o Launcher cria **ambientes 100% isolados** para cada conta. 
- Cada janela roda de forma independente com seu próprio diretório de cache de disco (`cache/user_email/cache`), eliminando travamentos de colisão de arquivo no Windows.
- Você pode abrir quantas contas desejar na grade e alternar entre elas com extrema fluidez.

---

## ⏰ 3. Auto-Relog Inteligente com Proteção de Eventos
Para manter o jogo sempre rápido e evitar o vazamento de memória RAM do Flash Player, o Launcher inclui o **Auto-Relog Inteligente**:

- **Proteção de Eventos Fictícios:** O Launcher **nunca** relogará durante os eventos principais do jogo (`11:00`, `13:00`, `15:00`, `17:00`, `19:00` e `21:35`).
- **Disparo Preventivo (15 minutos antes):** O relog é agendado para **15 minutos antes** dos eventos (`10:45`, `12:45`, `14:45`, `16:45`, `18:45` e `21:20`), garantindo RAM zerada no início da batalha.
- **Aviso de 15 Segundos (`RelogPromptDialog`):** Antes de executar o relog, uma janela avisará:
  - **[ ▶ Relogar Agora ]**: Executa a limpeza da RAM imediatamente.
  - **[ ⏰ Adiar +30 min ]**: Se você estiver em combate ou atividade, clique para adiar em 30 minutos.
  - **[ ✕ Cancelar ]**: Cancela o relog daquela rodada.
  - *Se você estiver ausente (AFK), ao expirar os 15s o jogo reloga sozinho!*

---

## 👻 4. Modo Stealth (Chefe Chegou!)
Precisa esconder o jogo rapidamente?
- Pressione **`Ctrl + Shift + A`** em qualquer lugar do computador.
- Instantaneamente, **TODAS** as janelas do jogo e o Hub desaparecerão da tela e da barra de tarefas.
- As janelas continuam rodando escondidas perto do relógio do Windows (na bandeja do sistema / System Tray).
- Para restaurar a visualização, pressione **`Ctrl + Shift + A`** novamente ou dê duplo clique no ícone do Javali perto do relógio.

---

## 🎯 5. Macros em Segundo Plano (Background Clicker)
As automações do Launcher injetam eventos diretamente no motor gráfico do jogo sem sequestrar o mouse do seu computador.

### A. AutoClicker Fantasma (F4)
1. Na janela do jogo, clique no menu de ferramentas (`🛠`) ou abra o painel flutuante (`⚡`).
2. Ative o **AutoClicker**.
3. Você terá **10 segundos** para posicionar o mouse sobre o local desejado.
4. O Launcher iniciará os cliques automáticos. **Você pode minimizar a janela do jogo e continuar usando o computador normalmente!**
5. Para parar a qualquer momento, pressione **F4**.

### B. Formação Mágica (Macro 5x5)
1. Ative a **Formação Mágica** pelo menu `🛠`.
2. Posicione o mouse no centro (X Vermelho) do tabuleiro durante a contagem regressiva de 5s.
3. O robô calculará a perspectiva isométrica e executará a sequência nos 25 pontos.

### C. Gravador de Macro Customizável (F7 / F8)
1. Pressione **F7** para iniciar a gravação. O título indicará "🔴 GRAVANDO MACRO...".
2. Realize os cliques e digitações no jogo.
3. Pressione **F7** novamente para salvar.
4. Pressione **F8** para reproduzir a automação.
5. Pressione **F4** para interromper.

---

## 🧹 6. Limpeza de Memória & Fast Relog Manual
Se quiser renovar a memória RAM da janela manualmente:
- **`🔄` Recarregar Página:** Atualiza a aba mantendo a sessão.
- **`🧹` Fast Relog (Limpeza de RAM):** Descarrega a aba para `about:blank`, aciona o *Garbage Collector* e a recarrega em menos de 1 segundo.
- **`🔇` Mudo Automático:** Clique no ícone de alto-falante para ativar ou desativar o áudio da aba.

---

## 🛡️ 7. Relatórios de Diagnóstico, Logs e Privacidade

### Onde ficam salvos os logs?
📂 `%LOCALAPPDATA%\LegendOnlineLauncher\launcher.log`  
*(C:\Users\<seu_usuario>\AppData\Local\LegendOnlineLauncher\launcher.log)*

### Privacidade Garantida
- **Senhas:** Jamais são gravadas nos arquivos de log.
- **E-mails:** São anonimizados automaticamente ao gravar no log (ex: `e******1@gmail.com`).

---

### ❓ Precisa de Suporte?
Se tiver dúvidas ou sugestões, acesse nosso **[Discord Oficial](https://discord.gg/d54VvTkdU5)** no canal `#dúvidas-e-ajuda`.
