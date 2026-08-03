# 📋 Checklist Definitivo de Integrações: Wartool ➔ BKLauncherLO

Este documento contém o mapeamento **100% exaustivo, auditado e definitivo** de **todas** as automações, atalhos, rotinas e configurações do **Wartool** (baseado na análise dos 499 arquivos de imagem `.bmp`, do arquivo `Settings.ini`, do arquivo `lang_Português.txt` e do script descompilado do AutoIt), organizadas por categoria para acompanhamento no **BKLauncherLO**.

---

## ⌨️ 0. Atalhos e Módulos Diretos do Wartool
- [ ] **Sylph Hunt Bot (`F2`):** Início automático da caça e farm de Sylphs no Atol.
- [ ] **Astral Clicker (`F4`):** Abertura, compra e sintetização automática de Astras.
- [ ] **AutoClicker Geral (`Ctrl+Shift+1`):** Spammer de cliques em qualquer botão selecionado.
- [ ] **Semi Auto CQ (`Shift+F4`):** Combate de Circuito semi-automático.
- [ ] **Weedbot / Horta (`Shift+F1`):** Tratar da horta, matar insetos e roubar frutos na fazenda.
- [ ] **Guild Spin (`Shift+F2`):** Giro automático da Roda da Guilda / Roda de Bênção (`Blessing Wheel`).
- [ ] **Combate de Tanques (`Ctrl+Shift+A`):** Disparo de habilidades e batalha em veículos/tanques.
- [ ] **Navegação nas Wilds (`Ctrl+E`):** Navegação e mapa no Território Selvagem.
- [ ] **Torre do Céu / Sky Trail (`Ctrl+Shift+2`):** Desafio e avanço de andares na Torre do Céu.
- [ ] **Auto-Combat (`Ctrl+Shift+C`):** Ativação de combate automático.
- [ ] **Arena de Grupo / Guardião (`Ctrl+Shift+4`):** Criação e entrada automática na sala da Arena.
- [ ] **Explorador da Dimensão de Ametista (`Ctrl+Shift+E`):** Navegação e mineração na Dimensão de Ametista.
- [ ] **Explorador Terrestre (`Ctrl+Shift+O`):** Navegação e tarefas terrestres.
- [ ] **World Boss (`Shift+F3`):** Entrada automática no Boss Mundial com ajuste de fuso horário.
- [ ] **Atoll Boss (`Ctrl+Shift+F`):** Entrada automática no Boss do Atol assim que a notificação gráfica aparecer.
- [ ] **Guild Boss (`Ctrl+Shift+3`):** Entrada e ataque automático no Boss da Guilda.
- [ ] **Controle de Execução:** Atalhos para pausar (`Ctrl+Shift+Z`) e encerrar (`Shift+Esc`).

---

## 🌾 1. Fazenda, Cultivo e Terreno
- [ ] **Auto-Colheita:** Leitura e colheita automática de plantas, frutos e árvores (`Farm_Ready`, `Farm_ReadyTree`, `v6FarmHouse`).
- [ ] **Auto-Replantio & Fusão:** Replantio e fusão automática de sementes (`Farm_Current`, `Farm_Meld`).
- [ ] **Limpeza de Ervas e Pragas:** Remoção de ervas e pragas em fazendas próprias e de amigos (`Farm_Weed`, `Farm_Bug`, `Farm_Sick`).
- [ ] **Tratamento de Plantas Mortas:** Reviver ou remover plantas secas (`Farm_Dead`, `Farm_ReviveIcon`).
- [ ] **Roubo de Frutos (`Roubar hortas`):** Roubo automático em fazendas de amigos (`Farm_Steal`, `Farm_StealIcon`).
- [ ] **Árvore da Vida & Conforto:** Energizar e dar conforto na Árvore da Vida (`Farm_EnergizeIcon`, `Farm_ComfortIcon`, `Farm_ToA`).
- [ ] **Cuidado de Animais:** Alimentação, ordenha e aplicação de pílulas em animais (`Farm_New_Feed`, `Farm_New_Milk`, `Farm_New_PillIcon`).

---

## ⛏️ 2. Mineração de Ametista e Caça de Joias
- [ ] **Coleta de Ametistas (`Amethyst Double Time`):** Mineração e transporte de Ametistas durante os horários de bônus do servidor.
- [ ] **Ciclo da Carroça de Ametista:** Carregamento e descarregamento automático da carroça de Ametista (`Amethyst_GetCart`, `Amethyst_Dump`).
- [ ] **Desvio de Monstros (`AvoidMonsters`):** Opção no `Settings.ini` para contornar monstros ou atacar monstros elite (`FightExpertMonsters`).
- [ ] **Caça de Joias (`JewelHunt`):** Automação do minijogo de busca e extração de joias.

---

## ⚔️ 3. Arena, PvP e Grupos
- [ ] **Auto-Criação de Salas:** Criação rápida de salas na Arena (`Arena_Create`, `Arena_CreateLODE`).
- [ ] **Gestão de Grupo e Crianças:** Aceite e convite automático de parceiros e crianças na sala (`PartyArena`, `KidArena`, `InParty`).
- [ ] **Auto-Pronto / Auto-Start:** Confirmação de prontidão assim que os slots são preenchidos (`Ready`, `Preparing`).

---

## 🐉 4. Atol dos Sylphs & Altar do Sacrifício
- [ ] **Auto-Navegação no Atol:** Entrada e movimentação pelos portais do Atol (`AtollEntrance1..3`, `AtollEntranceW`).
- [ ] **Caça de Sylphs por Elemento (`Sylph`):** Caça direcionada aos elementos Íris (Água), Amazonas (Vento), Eva (Fogo), Gaia (Terra), Pan e Asimas.
- [ ] **Modo Passear:** Movimentação aleatória pelo Atol sem rotas fixas.
- [ ] **Relocalização por Minimapa:** Reposicionamento periódico pelo minimapa para evitar travamentos em cantos do mapa.
- [ ] **Altar do Sacrifício de Sylphs (`Sac_1StarGrowth` / `Sac_Seal`):** Sacrifício e evolução de crescimento de Sylphs pelos selos de elemento.
- [ ] **Boss do Atol (`Sylph Boss`):** Detecção de aparecimento e convite/pedido de grupo para o Boss do Atol (`v5AtollBossAppeared`).
- [ ] **Passe de Evento Sem Matar:** Opção para permanecer no Atol apenas aguardando eventos sem atacar Sylphs normais.

---

## 🔄 5. Batalha de Circuito (Circuit)
- [ ] **Auto-Entrega de Missões do Circuito:** Entrega automática de fases do Circuito (`Circuit`, `Circuit_Deliver_Complete`).
- [ ] **Auto QTE do Circuito:** Acerto automático dos direcionais QTE no Circuito (`Circuit_QTE_A`, `Circuit_QTE_S`, `Circuit_QTE_D`, `Circuit_QTE_W`).
- [ ] **Encantamento e Soquetes do Circuito:** Melhora automática de equipamentos do circuito (`Circuit_Enchant`, `Circuit_Socket`).

---

## 🔮 6. Astras (Sistema de Astral)
- [ ] **Sintetização Automática (`AstralLoops`):** Definição do número de voltas antes de sintetizar Astras.
- [ ] **Filtro de Venda por Cor (`AstralSell`):** Venda automática de Astras de baixa qualidade (1-click sell).
- [ ] **Combinar Raras (`AstralSpecial`):** Opção para combinar Astras Vermelhas e Laranjas automaticamente.
- [ ] **Captura VIP / Chiron (`AstralVIP` / `AstralChiron`):** Invocação de Chiron e captura rápida de 1-clique para VIPs.

---

## 🏰 7. Torre do Céu, Catacumbas & Outlands
- [ ] **Torre do Céu (Sky Trail):** Avanço automático de andares (`v5Skytrail_Challenge`, `v5Skytrail_NextLvl`).
- [ ] **Sky City Loot:** Coleta de baús e saques caídos na Cidade do Céu sem caçar Sylphs.
- [ ] **Movimentação nas Wilds:** Navegação no Território Selvagem (`Wilds_Coords.txt`).

---

## 💥 8. Veículos / Tanques, Montaria & Bosses
- [ ] **Combate com Tanques (`DoTanks`):** Disparo de habilidades de tanques (`Tank_Attack`, `Tank_Laser`, `Tank_Shield`, `Tank_Acid`, `Tank_Spinal`).
- [ ] **Evolução de Montarias (`v5Beast1`):** Treinamento automático de montarias.
- [ ] **Batalha da Guilda & Boss da Guilda (`DoGB` / `DoGuildBoss`):** Entrada agendada na Guerra da Guilda e ataque ao Boss da Guilda (`Ctrl+Shift+3`).
- [ ] **World Boss (`DoWB`):** Entrada agendada no Chefe Mundial com desativação opcional de transformação para sobreviver ao ataque final.

---

## ⚙️ 9. Utilitários, Prevenção de Lag e Sistema
- [ ] **Sincronização de Fuso Horário (`Diferença Horária`):** Ajuste de tempo (-24h a +24h) em relação ao horário do servidor para acionamento pontual de eventos.
- [ ] **Auto-Resposta de PMs (`Responder a PMs`):** Leitura de chat privado e envio de respostas automáticas personalizadas.
- [ ] **Auto-Refresh Anti-Lag:** Atualização periódica da página do jogo a cada X minutos para reduzir o consumo de memória RAM do Flash Player.
- [ ] **Comprar Vida Automática (`Comprar HP`):** Compra automática de poções de HP na loja durante batalhas quando a vida fica baixa.
- [ ] **Modo Inverno / Neve (`Tema Inverno`):** Alternância automática para conjunto de gráficos de inverno (`AtollEntranceW`, `Farm_ToAWinter`).
- [ ] **Modo Turbo (Cliques Virtuais / Não usar mouse):** Envio de comandos de cliques diretos sem mover o ponteiro real do mouse.
- [ ] **Resgate de Recompensas Online (`OnlineRewards`):** Coleta automática de baús e prêmios por tempo de conexão.

---

> 📝 **Nota de Controle:** Marque com um `[x]` as automações conforme forem desenvolvidas e integradas na aba de macros/módulos do **BKLauncherLO**.
