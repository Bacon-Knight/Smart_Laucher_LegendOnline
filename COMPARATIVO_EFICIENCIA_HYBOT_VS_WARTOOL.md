# ⚔️ Relatório Comparativo de Eficiência: HyBot vs. Wartool

Este documento apresenta uma análise técnica profunda comparando as automações em comum entre o **HyBot** e o **Wartool**, avaliando em qual das duas ferramentas cada recurso é mais eficiente e por quê, fornecendo a base ideal para o desenvolvimento do **BKLauncherLO**.

---

## 📊 Quadro Resumo de Eficiência por Módulo

| Módulo / Automação | HyBot | Wartool | Ferramenta Mais Eficiente | Motivo Técnico |
| :--- | :---: | :---: | :---: | :--- |
| **🌾 Fazenda e Cultivo** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **HyBot** | Trata casos de erro (ratos, pragas, tempo de colheita ajustável) e tem filtro por nível de semente. |
| **🐉 Atol dos Sylphs (Farming)** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Wartool** | Possui relocalização automática por minimapa (evita travar nos cantos) e recortes de imagem por elemento. |
| **🔮 Astras e Cosmos** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Wartool** | Mais rápido, permite configurar loops de fusão (`AstralLoops`), velocidade e suporte 1-clique VIP. |
| **⚔️ Arena PvP (Solo / Grupo)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **HyBot** | Gerencia melhor a checagem de 3 slots de grupo (3v3), modo Assassino e reconvite automático. |
| **⛏️ Dimensão de Ametista** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Empate (Complementares)** | HyBot é melhor nas rotas de caminhada (`WALKSLEEP`); Wartool é melhor no agendamento por fuso horário. |
| **🔄 Batalha de Circuito (Circuit)** | ⭐⭐ | ⭐⭐⭐⭐⭐ | **Wartool** | Suporte completo a QTEs de teclado (W/A/S/D), encantamentos e soquetes de itens. |
| **⏰ Agendamento de Eventos** | ⭐⭐ | ⭐⭐⭐⭐⭐ | **Wartool** | Possui fuso horário editável (-24h a +24h) para entrada exata em World Boss, Guerra de Guilda e Ametista. |
| **⚡ Otimização Anti-Lag & Mouse** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Wartool** | Suporta cliques virtuais sem mover o mouse e Auto-Refresh periódico do Flash a cada X minutos. |

---

## 🔍 Análise Detalhada dos Módulos em Comum

### 1. 🌾 Fazenda e Horta (Vencedor: HyBot)
* **HyBot:** O HyBot possui um algoritmo mais maduro para a fazenda. Ele gerencia o tempo entre checagens via slider (`TempoFazenda`), elimina ratos no terreno (`GuiMataRato`), trata plantas mortas e permite escolher exatamente qual nível de semente replantar (`LvFazenda`).
* **Wartool:** O Wartool faz colheita e roubo de forma mais direta (via `Weedbot`), porém tem menos flexibilidade de recuperação se a planta secar ou se surgirem pragas.
* **Veredito para o BKLauncherLO:** Utilizar a lógica de decisões do **HyBot** combinada com os recortes de imagem do **Wartool**.

---

### 2. 🐉 Atol dos Sylphs (Vencedor: Wartool)
* **HyBot:** O HyBot faz a caça simples e contagem de limite diário, mas pode ficar preso nos cantos do mapa se a rota falhar.
* **Wartool:** O Wartool implementa duas soluções geniais:
  1. **Relocalização por Minimapa:** A cada X ciclos, ele clica no minimapa para reposicionar o personagem no centro, impedindo que o bot fique trancado em paredes.
  2. **Imagens Específicas por Elemento:** Possui variações de recortes para cada Sylph (Íris, Amazonas, Eva, Gaia, Pan, Asimas), reduzindo drasticamente falsos negativos.
* **Veredito para o BKLauncherLO:** Adotar a arquitetura de **relocalização por minimapa do Wartool**.

---

### 3. 🔮 Astras / Cosmos (Vencedor: Wartool)
* **HyBot:** O HyBot captura Astros de forma linear via `CosmoStart` / `Astral2`, podendo encher o inventário rapidamente.
* **Wartool:** O Wartool possui controles refinados no `Settings.ini`:
  * `AstralSpeed`: Ajuste da velocidade de clique.
  * `AstralLoops`: Número exato de voltas antes de sintetizar para não lotar a mochila.
  * `AstralSpecial`: Combinação automática de Astras Vermelhas e Laranjas.
* **Veredito para o BKLauncherLO:** Adotar as configurações de loop e velocidade do **Wartool**.

---

### 4. ⚔️ Arena PvP e Grupo (Vencedor: HyBot)
* **HyBot:** O HyBot é significativamente superior no gerenciamento de salas de Arena. Ele verifica a prontidão dos 3 jogadores na sala 3v3 antes de dar start, trata o modo Assassino (`AutoAssassinato`) e faz o ciclo de re-match de forma contínua.
* **Wartool:** O Wartool consegue criar e entrar em salas, mas o controle de confirmação de prontidão de terceiros é mais rígido e sujeito a falhas em partidas de grupo.
* **Veredito para o BKLauncherLO:** Implementar o fluxo de verificação de grupo do **HyBot**.

---

### 5. ⛏️ Dimensão de Ametista (Empate Técnico)
* **HyBot:** Excelente no controle do personagem dentro do mapa (`WALKSLEEP`), desvio de barreiras (`DimensionBreakBarrier`) e transporte da carroça de Ametista.
* **Wartool:** Excelente no agendamento (`Amethyst Double Time`), além de permitir escolher entre evitar monstros comuns (`AvoidMonsters`) ou focar em monstros elite (`FightExpertMonsters`).
* **Veredito para o BKLauncherLO:** **Unir as duas abordagens!** Usar o agendamento temporizado do Wartool com a navegação de rota do HyBot.

---

### 6. ⚡ Desempenho e Anti-Lag (Vencedor: Wartool)
* **Wartool:** Leva grande vantagem técnica em estabilidade:
  * **Auto-Refresh Anti-Lag:** Recarrega a página do jogo a cada X minutos para liberar o acúmulo de memória RAM do Flash Player.
  * **Cliques Virtuais:** Permite rodar ações sem mover o ponteiro real do mouse do sistema operacional.
* **HyBot:** Depende de cliques diretos na janela ativa.

---

## 🎯 Conclusão e Recomendação para o BKLauncherLO

Para criar a melhor ferramenta de automação do mercado, o **BKLauncherLO** não deve copiar apenas uma ferramenta, mas sim **mesclar o melhor de cada uma**:

1. **Do HyBot:** Importar a lógica da **Fazenda**, **Arena 3v3 / Grupo** e **Controle de Combos/Skills**.
2. **Do Wartool:** Importar o motor do **Atol dos Sylphs (com relocalização por minimapa)**, **Astras Clicker**, **Batalha de Circuito (QTEs)**, **Agendamento por Fuso Horário** e o **Auto-Refresh Anti-Lag**.
