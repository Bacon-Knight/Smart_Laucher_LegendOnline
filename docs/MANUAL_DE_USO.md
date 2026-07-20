# 📖 Manual de Uso - Bacon Knight Launcher

Bem-vindo ao manual oficial do **Bacon Knight Launcher (v2.2)**. Aqui você vai aprender a tirar o máximo de proveito do nosso sistema de multi-boxing, otimizações de performance, automação e stealth.

---

## 🚀 1. Primeiros Passos e Login
1. Ao abrir o aplicativo, você verá o **Hub de Contas** com formulário e cartões visuais.
2. Preencha seus dados de acesso (E-mail e Senha) e escolha o Servidor.
3. (Opcional) Digite um apelido/nick para organizar suas contas (ex: "Arqueiro Principal").
4. Clique em **"Salvar e Adicionar Conta"**. A conta aparecerá na grade de cartões.
5. Para jogar, basta clicar em **"▶ Entrar"** no cartão da conta. O Launcher fará o login automático para você!

---

## ⚡ 2. O Poder do Multi-Boxing (Várias Contas Simultâneas)
Ao contrário de navegadores normais que misturam cookies ou desconectam contas simultâneas, o Launcher cria **ambientes isolados** para cada conta. 
- Você pode abrir quantas contas desejar na grade e clicar em "Entrar" em todas elas.
- Cada janela roda de forma independente com seu próprio perfil de dados, enquanto compartilha o cache de imagens/SWF para economizar banda da sua internet.

---

## 👻 3. Modo Stealth (Chefe Chegou!)
Precisa esconder o jogo rapidamente?
- Pressione **`Ctrl + Shift + A`** em qualquer lugar do computador.
- Instantaneamente, **TODAS** as janelas do jogo e o Hub desaparecerão da tela e da barra de tarefas.
- As janelas continuam rodando escondidas perto do relógio do Windows (na bandeja do sistema / System Tray).
- Para restaurar a visualização, pressione **`Ctrl + Shift + A`** novamente ou dê duplo clique no ícone do Javali perto do relógio.

---

## 🎯 4. Macros em Segundo Plano (Background Clicker)
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

### D. Auto-Luta Inteligente (F5 / Shift+F5)
1. Pressione **Shift+F5** para configurar a sequência de teclas do seu personagem (ex: `1 2 3 4 5` ou `1 s 2 q`).
2. Pressione **F5** para ativar o Auto-Luta. O algoritmo detectará quando seu personagem entrar em combate e disparará a sequência automaticamente.

---

## 🧹 5. Limpeza de Memória & Fast Relog
Se for manter o jogo aberto por muitas horas seguidas, utilize os botões da barra de título da janela do jogo:
- **`🔄` Recarregar Página:** Atualiza a aba mantendo a sessão.
- **`🧹` Fast Relog (Limpeza de RAM):** Descarrega a aba da memória e a recarrega em menos de 1 segundo, ativando o Garbage Collector para liberar memória RAM ocupada pelo plugin Flash.
- **`🔇` Mudo Automático:** Clique no ícone de alto-falante para ativar ou desativar o áudio da aba.

---

## 🛡️ 6. Relatórios de Diagnóstico, Logs e Privacidade

### Onde ficam salvos os logs?
Os arquivos de log do aplicativo são salvos automaticamente na pasta do sistema:  
📂 `%LOCALAPPDATA%\LegendOnlineLauncher\launcher.log`  
*(C:\Users\<seu_usuario>\AppData\Local\LegendOnlineLauncher\launcher.log)*

### Privacidade Garantida
- **Senhas:** Jamais são gravadas nos arquivos de log.
- **E-mails:** São anonimizados automaticamente ao gravar no log (ex: `e******1@gmail.com`), permitindo que você compartilhe os logs para suporte técnico sem expor seus dados.

### Notificação de Crash
Se o jogo ou o Launcher sofrer um encerramento inesperado, ao reabrir a aplicação uma janela avisará o ocorrido mostrando o código do erro (ex: `ERR-QT-501`) e disponibilizará o botão **"📁 Abrir Pasta do Log"** para abrir diretamente a pasta no Windows Explorer.

---

### ❓ Precisa de Suporte?
Se tiver dúvidas ou sugestões, acesse nosso **[Discord Oficial](https://discord.gg/d54VvTkdU5)** no canal `#dúvidas-e-ajuda`.
