# Roadmap (Plano de Futuro)

Ideias, metas e pendências para o futuro do Launcher. Este arquivo guia o desenvolvimento futuro do projeto.

## Portabilidade para Linux (Ubuntu / Debian)
**O Desafio:**
No Linux, o `pepflashplayer.dll` do Windows não funciona. A biblioteca do Qt WebEngine precisará carregar a versão em `.so` correspondente (ex: `libpepflashplayer.so`).

**Plano de Execução:**
- Alterar o `launcher.py` na injeção de plugin:
  ```python
  import platform
  if platform.system() == "Windows":
      plugin_path = resource_path("pepflashplayer.dll")
  elif platform.system() == "Linux":
      plugin_path = resource_path("libpepflashplayer.so")
  ```
- No Linux, garantir que as bibliotecas `libnss3` e pacotes do Qt5 WebEngine (`python3-pyqt5.qtwebengine`) estejam instalados no SO hospedeiro, ou empacotados num `.AppImage`.

## Novas Ferramentas e Macros
- **Capturador de Imagem In-Game:** Uma ferramenta que permite tirar prints do jogo internamente e salvar numa pasta de "Telas de Vitória".
- **Botões Dinâmicos Flutuantes:** Permitir que o usuário crie botões de macros customizados de auto-clique coordenado, onde ele arrasta o botão na tela sobre a área que deseja macro de farm, definindo a taxa de atualização.
- **Relatório de Desempenho:** Adicionar opção para monitorar e reportar o ping de resposta do servidor, auxiliando no timing perfeito dos combates de PvP.

## UI/UX
- **Painel de Gerenciamento de Contas Avançado:** Hoje usamos um ComboBox. Criar uma tela dedicada no `LauncherHub` (uma grid) que exibe as contas em forma de "Cartões", mostrando status, tempo de última vez jogada e nome do personagem.
- **Botão Fixar:** Permitir "Pinar" uma aba na frente das outras, muito útil quando se joga com a tela dividida.
