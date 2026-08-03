# 📋 Checklist Definitivo de Integrações: HyBot ➔ BKLauncherLO

Este documento é a compilação **100% exaustiva e absoluta** de **todas as automações e rotinas** extraídas do código-fonte do **HyBot** (`HyBot_codigo_limpo.ahk`, `HyBot_extraido.ahk` e dumps de memória do executável). Nenhuma funcionalidade foi omitida.

---

## 🌾 1. Fazenda, Cultivo e Terreno
- [ ] **Auto-Colheita (`Fazenda` / `Pastos` / `inicio_pastos`):** Leitura e colheita automática de frutos e sementes maduras.
- [ ] **Auto-Replantio por Nível (`LvFazenda` / `Replantar` / `PlantChoice`):** Seleção e replantio automático de sementes conforme o nível da fazenda.
- [ ] **Limpeza de Ervas e Pragas (`Farm_Weed` / `Farm_Bug`):** Remoção de pragas e ervas daninhas em plantas próprias e de amigos.
- [ ] **Roubo de Frutos em Amigos (`FarmCollect` / `Farm_Steal`):** Invasão automática e coleta de frutos na fazenda de amigos.
- [ ] **Eliminação de Ratos e Pragas (`inicio_rato` / `GuiMataRato`):** Varredura e eliminação automática de ratos no terreno da fazenda.
- [ ] **Árvore da Vida (`NovoPasto` / `MenuFazenda`):** Energização, rega e bônus na Árvore da Vida.
- [ ] **Controle de Frequência de Coleta (`TempoFazenda`):** Slider para ajuste de velocidade e delay entre os ciclos de checagem.

---

## ⛏️ 2. Dimensão & Minas de Ametista (`[Planos]`)
- [ ] **Mineração na Dimensão Império (`AutoBDI` / `AutoBDICharDetect`):** Navegação, mineração de Ametista e transporte na Dimensão Império.
- [ ] **Mineração na Dimensão Vento (`AutoBDV` / `QuitBDV`):** Navegação e coleta na Dimensão Vento.
- [ ] **Mineração na Dimensão Água (`AutoBDA`):** Navegação e mineração na Dimensão Água.
- [ ] **Mineração na Dimensão Atenas/Fogo (`AutoBDAt` / `AutoBDITower`):** Navegação e mineração na Dimensão de Atenas/Fogo.
- [ ] **Busca de Transmissor e Barreira (`CheckTransmissor` / `DimensionBreakBarrier` / `BGBreakBarrier`):** Localização de transmissores e destruição de barreiras no mapa da dimensão.
- [ ] **Ciclo da Carroça de Ametista (`Amethyst_Ore` / `Amethyst_GetCart` / `Amethyst_Dump`):** Coleta dos minérios, carregamento da carroça e descarregamento automático na base.
- [ ] **Ajuste de Caminhada e Velocidade (`WALKSLEEP` / `BGWalk` / `DimensionWalk`):** Configuração de rota e tempo de passos baseado na classe (`Class`), gênero (`Gender`) e velocidade do personagem.

---

## ⚔️ 3. Combate, Skills e Personagem
- [ ] **Rotação de Combos (`Save1` / `Save2` / `Save3` / `CombatePlan`):** Execução sequencial de atalhos de habilidades (Z, X, 1, 2, 3, 4, 5) em 3 perfis configuráveis.
- [ ] **Ajuste de Delay de Ataque (`TempoCombo`):** Ajuste de tempo de espera entre rajadas de habilidades.
- [ ] **Auto QTE (`inicio_QTE` / `GuiQTE` / `QTE`):** Execução automática de comandos rápidos de tela durante combos.
- [ ] **Modo Ilha e Einherjar (`Ilha` / `SylphTransformer` / `IlOk2`):** Ativação e rotação automática da transformação de Einherjar.
- [ ] **Troca de Runas e Guardas (`RunaZ`, `RunaX`, `Guarda2`):** Invocação e alternância de Runas e Guardas no meio da luta.
- [ ] **Controle de Cooldown / Desperdício (`ArDesp` / `ArDespText`):** Temporização para prevenir desperdício de turnos.

---

## 🏆 4. Eventos PvP, Guerras e Arenas
- [ ] **Arena Solitária (`Arenas` / `inicio_arena` / `AutoArena`):** Entrada e desafio automático na Arena 1v1.
- [ ] **Arena de Grupo (`CfgArenaG` / `ArenaSylph`):** Formação de salas, convite e entrada automática em Arena 3v3 / Grupo.
- [ ] **Auto-Matchmaking & Ready:** Leitura visual dos slots da sala para confirmação automática de "Pronto" e "Iniciar".
- [ ] **Modo Auto-Assassinato (`AutoAssassinato` / `CfgAutoAssassinato`):** Entrada e combate contínuo no modo Assassino.
- [ ] **Chamas Imortais (`AutoChamas` / `ChamasAtaque` / `EasyChamasAtaque`):** Entrada, combate e coleta de Chamas Imortais.
- [ ] **Guerras Diárias e Semanais (`AutoWeeklyWars` / `WeeklyWars`):**
  - [ ] **Guerra Imperial (`ImperialWar` / `ImperialWarDay`)**
  - [ ] **Guerra de Ares (`AresWar` / `AresWarDay` / `AresWarCombate`)**
  - [ ] **Guerra de Atenas (`AthenasWar` / `AutoAthenasWar`)**
  - [ ] **Guerra de Vênus (`VenusWar` / `AutoVenusWar` / `VenusWarChest`)**
  - [ ] **Batalha do Caos e Servidores (`BGCS2` / `CS2` / `CSLAR`)**

---

## 🐉 5. Atol dos Sylphs
- [ ] **Navegação e Caça no Atol (`AutoSylphIsland` / `SylphIsland` / `SylphIslandSave`):** Entrada, busca e movimentação pelos andares do Atol.
- [ ] **Captura de Sylphs com Limite Diário (`SylphLimit1` / `SylphLimit2`):** Captura contínua de Sylphs selvagens até atingir os limites diários.
- [ ] **Busca de Alvo/Sylph Raro (`SwapTargetSylph1` a `4` / `SwapActiveSylph`):** Seleção de alvos específicos de Sylphs de alto valor.

---

## 🏛️ 6. Instâncias PVE, Torres e Labirinto
- [ ] **Labirinto / Torre das Ilusões (`AutoLabyrinth` / `AutoLabyrinthUseKey`):** Progresso no labirinto com uso automático de chaves (`AutoLab1Key` a `3Key`).
- [ ] **Campanha de Grupo / Dungeons (`AutoCG` / `AutoMultiplayer` / `CfgAutoCG`):** Criação e entrada automática em instâncias de grupo.
- [ ] **Torre do Tempo / Portal do Tempo (`AutoTM` / `TimePortal` / `TimePortalBoss` / `TimePortalStrong`):** Desafio e avanço na Torre do Tempo.
- [ ] **Salão de Atividades & SkyTrail (`AutoActivities` / `AutoActivitiesSkyTrail` / `AutoActivitiesSylph`):** Execução automática das tarefas do Salão de Atividades e Torre do Céu.

---

## 🏰 7. Guilda, Cidade e Porto
- [ ] **Oração da Guilda / Leida (`AutoLeida` / `RegisterLeida` / `GBless` / `GuildBless`):** Execução de bênçãos/orações e registro automático.
- [ ] **Chefe da Guilda (`GuildBoss`):** Ataque automatizado e ressuscitação rápida contra o Boss de Guilda.
- [ ] **Loja do Porto e Navegação (`HarborTrade` / `LojaNave` / `VoyageShop` / `VoyageCapture`):** Aceite de rotas marítimas, rejeição de viagens ruins (`NewVoyageReject`) e compra automática de itens.
- [ ] **Toca de Monstros e Recompensas (`Toca` / `TocaStart` / `BountySpot`):** Aceite e execução de missões de recompensa na Toca de Monstros.

---

## 🔮 8. Cosmos, Astras e Eremitério
- [ ] **Cosmos / Astras (`Cosmo` / `CosmoStart` / `Astral2` / `OCAstral` / `BGAstral2`):** Captura de Astros/Cosmos de nível 2, organização e fusão automática.
- [ ] **Eremitério / Santuário do Einherjar (`Eremiterio` / `Eremiterio2` / `EremiterioSubmit`):** Doação diária de recursos e aprimoramento de bênçãos no Eremitério.

---

## 🐱 9. Gato da Sorte, Casa, Arqueologia e Contratos
- [ ] **Gato da Sorte / Casa dos Gatos (`AutoCatHouse` / `ItemGato1` a `5`):** Troca automática de até 5 itens configurados no Gato da Sorte.
- [ ] **Residência / Casa de Casal (`AutoResid`):** Tarefas diárias e manutenção da residência.
- [ ] **Resgate de Presentes e Pacotes Online (`Presentes` / `AutoPct` / `OnlinePackage`):** Coleta automática de presentes, logins e pacotes de tempo online.
- [ ] **Roleta Diária (`Roleta` / `VRoulette`):** Giros automáticos na roleta de prêmios.
- [ ] **Auto-Arqueologia (`Arqueologia` / `ArqueoRestart` / `OTLSearch` / `OTLLook`):** Mapeamento, escavação e troca de pás em pontos de Arqueologia.
- [ ] **Bênção do Contrato dos Elfos (`ContratoElfos` / `Elfos`):** Ativação e renovação automática da bênção do Contrato dos Elfos.

---

## ⚙️ 10. Utilitários, Monitoramento e Sistema
- [ ] **Benefícios e Coleta VIP (`VIPClick` / `NewVipClick`):** Coleta automática diária de baús VIP.
- [ ] **Monitor de Lag e Ping (`LAGMonitor` / `Ping` / `PingOk` / `ChangePingServer`):** Medição de latência e reinicialização de rotinas caso ocorra travamento/lag.
- [ ] **Troca de Personagem / Multi-Contas (`MultiAccount` / `MultiAccountSylph`):** Alternância automática entre contas salvas.
- [ ] **Auto-Desligamento (`Desligar`):** Encerramento do jogo e desligamento do computador após concluir a rotina.
- [ ] **Gerenciamento de Atalhos Teclado (`SHORTCUTS` / `Pause` / `More`):** Atalhos customizáveis para pausar (`F1`) ou expandir o bot.
- [ ] **Suporte Multilingue (`PT-br`, `EN-us`, `ES-es`):** Troca dinâmica de idioma da interface.

---

> 📝 **Nota de Controle:** Marque com um `[x]` as automações conforme forem sendo desenvolvidas e integradas na aba de macros/módulos do **BKLauncherLO**.
