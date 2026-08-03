# 🏆 Checklist Mestre Unificado: Automações HyBot, Wartool & Repositórios GitHub ➔ BKLauncherLO

Este é o documento mestre definitivo contendo **todas as automações** mapeadas do **HyBot**, **Wartool** e dos **Repositórios do GitHub** (`pyWartune`, `Wartune-AutoIt`, `wartune-automation`, `WarTuneLogin`, `WartuneUltraSlyphAutomation`). 

Nas automações **em comum**, a lista já seleciona e recomenda a **implementação da ferramenta mais eficiente**, garantindo que o **BKLauncherLO** receba o estado da arte de cada módulo.

---

## 🌾 1. Módulo: Fazenda, Cultivo e Terreno
*Fonte Selecionada: **HyBot** (Maior tolerância a falhas, pragas e controle de sementes)*
- [Implementar] **Auto-Colheita:** Identificação e colheita automática de frutos e sementes maduras.
- [Implementar] **Auto-Replantio por Nível:** Seleção e replantio automático de sementes conforme o nível da fazenda (`LvFazenda`).
- [Implementar] **Limpeza de Ervas e Pragas:** Remoção automática de ervas daninhas e pragas/vermes em plantas próprias e de amigos.
- [Implementar] **Eliminação de Ratos e Pragas (`GuiMataRato`):** Varredura e eliminação automática de ratos no terreno da fazenda.
- [Implementar] **Roubo de Frutos em Amigos:** Invasão automática e coleta de frutos na fazenda de amigos.
- [Implementar] **Árvore da Vida & Conforto:** Energizar, dar conforto e regar a Árvore da Vida (`Farm_ToA`).
- [Implementar] **Cuidado de Animais (Wartool):** Alimentação, ordenha e pílulas em animais (`Farm_New_Feed`, `Farm_New_Milk`).
- [Implementar] **Ajuste de Tempo e Delay:** Slider de velocidade e controle de delay entre checagens da fazenda (`TempoFazenda`).

---

## 🏛️ 2. Módulo: Edifícios, Academia e Cidade Principal (`pyWartune` Exclusivo)
*Fonte Selecionada: **pyWartune** (Automação completa da infraestrutura da cidade)*
- [ ] **Upgrade Automático da Cidade (`runTown` / `UpgradeBuilding`):** Melhoria automática da Prefeitura, Fazenda, Quartel e Altar.
- [ ] **Academia de Tecnologias (`runAcademy`):** Consumo e upgrade automático das tecnologias da Academia (Ataque, Defesa, Vida e Tropas).
- [ ] **Navegação na Cidade das Nuvens (`runCloudCity`):** Acesso e navegação automática na Cloud City.
- [ ] **Reset Diário de Instâncias (`runReset`):** Redefinição automática das rotinas diárias ao virar o dia do servidor.

---

## 🐉 3. Módulo: Atol dos Sylphs (Caça & Farm)
*Fonte Selecionada: **Wartool + WartuneUltraSlyphAutomation** (Relocalização por minimapa + OpenCV)*
- [Implementar] **Relocalização por Minimapa (Anti-Trava):** Reposicionamento periódico pelo minimapa para evitar que o boImplementart fique preso em cantos/obstáculos do Atol.
- [Implementar] **Reconhecimento por Visão Computacional (OpenCV):** Uso do algoritmo `cv2.matchTemplate` para captura ultrarrápida de Sylphs sem falsos positivos.
- [Implementar] **Captura de Sylphs por Elemento Direcionado:**
  - [Implementar] **Íris (Água):** Caça automática de Íris Nível 1 a 6 (`IrisL1..6`).
  - [Implementar] **Amazonas (Vento):** Caça automática de Amazonas Nível 1 a 9 (`AmazonL1..9`).
  - [Implementar] **Eva (Fogo):** Caça automática de Eva Nível 1 a 5 (`EveL1..5`).
  - [Implementar] **Gaia (Terra):** Caça automática de Gaia Nível 1 a 5 (`GaiaL1..5`).
  - [Implementar] **Pan / Asimas:** Caça automática de Pan e Asimas (`PanL1..3`, `Asimas`).
- [Implementar] **Modo Passear (Wartool):** Movimentação aleatória pelo Atol sem rotas engessadas.
- [Implementar] **Controle de Limite Diário (HyBot):** Parar caça ao atingir os limites diários (`SylphLimit1`/`SylphLimit2`).
- [Implementar] **Atol Boss:** Entrada e ataque automatizado ao Boss do Atol assim que a notificação gráfica surgir (`v5AtollBossAppeared`).
- [Implementar] **Altar do Sacrifício de Sylphs (Wartool):** Sacrifício e evolução de crescimento de Sylphs pelos selos de elemento (Água, Fogo, Vento, Elétrico).

---

## 🔮 4. Módulo: Cosmos e Astras (Astral Clicker)
*Fonte Selecionada: **Wartool + wartune-automation** (Loops ajustáveis e thread dedicada em Python)*
- [Implementar] **Sintetização por Loops Ajustáveis (`AstralLoops`):** Definição do número exato de voltas antes de sintetizar para não lotar o inventário.
- [Implementar] **Filtro de Venda por Cor (`AstralSell`):** Venda rápida automática de Astras de baixa qualidade.
- [Implementar] **Combinação de Raras (`AstralSpecial`):** Fusão automática de Astras Vermelhas e Laranjas.
- [Implementar] **Captura VIP / Chiron (`AstralVIP` / `AstralChiron`):** Invocação automática de Chiron com suporte a clique único VIP.
- [Implementar] **Ajuste de Velocidade (`AstralSpeed`):** Slider para controle de velocidade de cliques na janela de Astras.

---

## ⚔️ 5. Módulo: Arena PvP, Combos e Modos de Grupo
*Fonte Selecionada: **HyBot + Wartune-AutoIt** (Leitura de 3 slots + Modo Seguir)*
- [Implementar] **Rotação de Combos de Skills (HyBot):** Execução sequencial de atalhos (Z, X, 1, 2, 3, 4, 5) em 3 perfis configuráveis (`Save1..3`).
- [Implementar] **Auto QTE:** Execução automática de comandos rápidos de tela durante combos.
- [Implementar] **Transformação Einherjar (`Ilha`):** Ativação e rotação automática de transformação de Einherjar.
- [Implementar] **Troca de Runas e Guardas:** Alternância de Runas (`RunaZ`/`RunaX`) e Guardas (`Guarda2`) em combate.
- [Implementar] **Arena Solitária (1v1):** Desafio e entrada rápida na Arena 1v1.
- [Implementar] **Arena de Grupo (3v3):** Formação de salas, convite de parceiros e verificação de prontidão dos 3 membros antes do início.
- [Implementar] **Modo Seguir Líder (`___following_mode` - AutoIt Exclusivo):** Acompanhar automaticamente o líder do grupo em instâncias e mapas PvP/PvE.

---

## ⛏️ 6. Módulo: Minas de Ametista & Dimensão (Planos)
*Fonte Selecionada: **Híbrida** (Agendamento do Wartool + Rotas de caminhada do HyBot)*
- [Implementar] **Mineração por Dimensão (HyBot):** Suporte às dimensões Império (`BDI`), Vento (`BDV`), Água (`BDA`) e Atenas/Fogo (`BDAt`).
- [Implementar] **Busca de Transmissor e Barreiras (HyBot):** Destruição automática de barreiras e acionamento de transmissores.
- [Implementar] **Ciclo da Carroça de Ametista:** Extração de minérios (`Amethyst_Ore`), carregamento da carroça (`Amethyst_GetCart`) e descarregamento na base (`Amethyst_Dump`).
- [Implementar] **Desvio de Monstros (Wartool):** Opção para contornar monstros comuns (`AvoidMonsters`) ou focar em monstros elite (`FightExpertMonsters`).
- [Implementar] **Ajuste de Passos (`WALKSLEEP` - HyBot):** Rota de caminhada personalizada conforme classe, gênero e velocidade.

---

## 🔄 7. Módulo: Batalha de Circuito (Circuit)
*Fonte Selecionada: **Wartool** (Automação completa dos QTEs W/A/S/D e equipamentos)*
- [Implementar] **Auto-Entrega do Circuito:** Leitura e entrega automática de fases do Circuito (`Circuit_Deliver_Complete`).
- [Implementar] **Auto QTE Direcional:** Acerto automático dos comandos de direção QTE (`W`, `A`, `S`, `D`) durante o circuito.
- [Implementar] **Encantamento e Soquetes:** Melhora automática de equipamentos do circuito (`Circuit_Enchant`, `Circuit_Socket`).

---

## ⏰ 8. Módulo: Agendamento de Eventos e Guerras
*Fonte Selecionada: **Wartool** (Sincronizador de Fuso Horário)*
- [Implementar] **Sincronização de Fuso Horário (-24h a +24h):** Ajuste de horário do servidor para entrada exata nos eventos programados.
- [Implementar] **World Boss:** Entrada automática no Chefe Mundial agendado com desativação opcional de transformação para sobreviver ao golpe final.
- [Implementar] **Guerras Diárias e Semanais (HyBot):** Entrada em Guerra Imperial, Ares, Atenas, Vênus e Caos.

---

## 🏰 9. Módulo: Guilda, Cidade e Porto
*Fonte Selecionada: **Híbrida** (Inclusão de recursos exclusivos de todas as fontes)*
- [Implementar] **Oração da Guilda / Leida (HyBot):** Oração automática com registro programado (`RegisterLeida`).
- [Implementar] **Altar da Guilda (Wartool + wartune-automation):** Doação diária e bênção ativada no Altar da Guilda (`guildaltar.py`).
- [Implementar] **Chefe da Guilda (`GuildBoss`):** Ataque automatizado e ressuscitação rápida contra o Boss de Guilda.


---

## 🐱 10. Módulo: Gato da Sorte, Casa, Tesouros e Eventos Especiais
- [ ] **Roda VIP (`___VIP_wheel` - AutoIt Exclusivo):** Giro diário na roleta de recompensas VIP.
- [ ] **Formação Mágica Inteligente (Exclusivo BKLauncherLO):** Automação tática de 3 passos no tabuleiro 5x5 com validação de 16 monstros, ativação dos Globos Verde 💚 e Azul 💙, ataque ao centro em asterisco (6.030 pts) até bater a meta de 24.000 pontos.

---

## 🛠️ 11. Módulo: Desempenho, Sistema e Anti-Lag
*Fonte Selecionada: **Wartool + WarTuneLogin** (Cliques virtuais, login automático e anti-lag)*
- [ ] **Auto-Refresh Anti-Lag (Wartool):** Recarga periódica da página do jogo a cada X minutos para liberar acúmulo de memória RAM do Flash Player.
- [ ] **Modo Turbo / Cliques Virtuais (Wartool):** Envio de eventos de clique diretamente para o processo sem mover o ponteiro real do mouse.
- [ ] **Login Automático com Rotação Anti-Ausência (WarTuneLogin):** Sistema de login automático transparente que mantém a conta ativa sem cair por AFK (`walkinCircle`).
- [ ] **Prevenção de AFK (Wartool):** Prevenção automática de desconexão por inatividade (`AFK.bmp`).
- [ ] **Auto-Resposta de PMs (Wartool):** Leitura de chat privado e envio de respostas automáticas personalizadas.
- [ ] **Monitor de Lag e Ping (HyBot):** Medição de latência com reinicialização automática de rotinas caso ocorra travamento.
- [ ] **Multi-Contas / Alternância (HyBot):** Alternância automática entre contas salvas.
- [ ] **Auto-Desligamento (`Desligar`):** Encerramento do aplicativo e desligamento do PC após concluir as rotinas.

---

> 📝 **Nota de Controle:** Marque com um `[x]` as automações conforme forem desenvolvidas e integradas na interface do **BKLauncherLO**.
