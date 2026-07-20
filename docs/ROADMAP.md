# 🗺️ Roadmap (Plano de Futuro & Conclusões)

Este documento registra as metas concluídas e os próximos passos para o futuro do **Bacon Knight Launcher**.

---

## ✅ Funcionalidades Concluídas (v2.1+)

- [x] **Painel de Gerenciamento de Contas em Cartões (Grid):** Tela dedicada no `LauncherHub` exibindo as contas salvas em cartões visuais com informações de servidor, nick, e-mail e atalhos rápidos de 1 clique.
- [x] **Relatório de Desempenho e Ping em Tempo Real:** Indicador de ping HTTP integrado à barra de título da janela do jogo, atualizado continuamente em thread secundária.
- [x] **Sistema de Notificação de Crashes & Diagnóstico:** Rastreamento global de erros não tratados com atribuição de códigos estruturados (`ERR-QT-501`, `ERR-NET-400`, `ERR-MEM-500`) e notificação visual com botão "📁 Abrir Pasta do Log" ao reabrir o app.
- [x] **Otimização Extrema de Memória V8 & GPU:** Expansão do heap V8 do Chromium para 2048 MB (fim do lag aos 15 min), ativação de aceleração gráfica por GPU e leitor recortado do Auto-Luta (`crop_rect`).
- [x] **Anonimização de Privacidade nos Logs:** Mascaramento automático de endereços de e-mail em logs de diagnóstico (`mask_email`).
- [x] **Fast Relog com Garbage Collection:** Limpeza instantânea de RAM (`gc.collect()`) ao descarregar a aba do jogo.

---

## 🐧 Portabilidade para Linux (Ubuntu / Debian)

**O Desafio:**
No Linux, o plugin PPAPI do Windows (`pepflashplayer.dll`) não é executado nativamente. O Qt WebEngine no Linux exige a biblioteca nativa `.so` (`libpepflashplayer.so`).

**Plano de Execução:**
1. Manter a detecção de plataforma em `src/main.py`:
   ```python
   if sys.platform == 'win32':
       plugin_path = resource_path("pepflashplayer.dll")
   else:
       system_plugin = "/usr/lib/pepperflashplugin-nonfree/libpepflashplayer.so"
       if os.path.exists(system_plugin):
           plugin_path = system_plugin
       else:
           plugin_path = resource_path("libpepflashplayer.so")
   ```
2. Fornecer script de empacotamento `.AppImage` ou script de build para sistemas baseados em Debian/Ubuntu (`build_fixed.sh`).

---

## 🔮 Próximas Funcionalidades Planejadas

- [ ] **Capturador de Imagem In-Game (Print Screen Rápido):** Ferramenta dedicada no menu de ferramentas para salvar capturas de tela das batalhas diretamente em uma pasta de vitórias.
- [ ] **Botões Fixadores (Pin Window):** Permitir "Pinar" uma janela de jogo sempre no topo (*Always on Top*), facilitando o acompanhamento durante partidas em tela dividida.
- [ ] **Gravador de Sequências de Teclas Avançado:** Interface visual para editar o delay individual entre teclas no Auto-Luta.
