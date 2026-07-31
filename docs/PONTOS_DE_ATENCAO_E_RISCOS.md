# Pontos de Atenção e Riscos — Legend Online Bacon Knight Launcher

Documento gerado em: 31/07/2026  
Escopo: análise estática do código-fonte em `src/` e dependências relacionadas.

---

## Críticos

### Webhook Discord exposto no código
- URL completa hardcoded em `src/services/feedback_service.py`
- Qualquer pessoa com acesso ao repositório pode enviar mensagens ao canal de suporte
- Risco de spam, abuso ou vazamento do endpoint

**Mitigação sugerida:** mover para variável de ambiente (`DISCORD_WEBHOOK_URL`), rotacionar o webhook atual e remover a URL do histórico Git se o repositório for público.

### Credenciais em texto plano
- E-mails e senhas persistidos no `QSettings` sem criptografia
- Acessíveis localmente por qualquer processo/usuário com permissão no perfil Windows

**Mitigação sugerida:** criptografar senhas com `keyring` / DPAPI do Windows, ou ao menos não persistir a senha e exigir reentrada por sessão.

### Injeção de login via JavaScript
- Credenciais inseridas diretamente no DOM da página do jogo
- Dependem da confiança no domínio `lobr.creaction-network.com` e de scripts de terceiros carregados na página

**Mitigação sugerida:** documentar o risco ao usuário; evitar logar credenciais; validar origem da página antes da injeção.

---

## Altos

### Código legado duplicado
- `src/ui/launcher_hub.py` e `src/ui/game_window.py` coexistem com `src/ui/views/hub_view.py` e `src/ui/views/game_view.py`
- O fluxo ativo (`src/main.py`) usa apenas a versão MVC em `ui/views/`
- Risco de corrigir bug em um arquivo e esquecer o outro

**Mitigação sugerida:** remover ou arquivar os arquivos legados após confirmar que nenhum spec/build os referencia.

### Duas estratégias de persistência de contas
- `HubController` usa chave `"saved_accounts"` (dict JSON)
- `AccountService` usa chave `"accounts"` (lista tipada `Account`)
- `AccountService` é instanciado mas não é o caminho principal de leitura/escrita

**Mitigação sugerida:** unificar em um único serviço e migrar dados existentes na primeira execução.

### Cache Proxy HTTP não conectado ao WebEngine
- `CacheProxyServer` sobe na porta 8124 em `src/main.py`
- Não há `setHttpProxy` / `QNetworkProxy` configurado no `QWebEngineProfile`
- O tráfego do jogo **não passa** pelo proxy — funcionalidade aparente, mas ineficaz
- O cache que funciona hoje é o do Chromium via `setCachePath(shared_cache_dir)`

**Mitigação sugerida:** conectar o proxy ao profile do WebEngine ou remover o servidor e a UI de status associada.

### Serviços implementados mas não integrados
- `OasApiService` (`src/services/oas_api_service.py`) — sem referências no fluxo principal
- `SessionCookieExtractor` (`src/services/session_service.py`) — idem
- Código preparatório pode divergir da implementação real quando for conectado

**Mitigação sugerida:** integrar na UI (seleção dinâmica de servidores) ou remover até estar pronto.

---

## Médios

### Inconsistência de versões
| Fonte | Versão |
|-------|--------|
| `README.md` | v2.3 |
| `src/ui/views/hub_view.py` (`CURRENT_APP_VERSION`) | 2.4 |
| `version_info.txt` / `installer.iss` | 2.4.1 |
| `feedback_service.py` / `LegendOnlineLauncher_v3.4.spec` | 3.4 |

- Update checker pode comparar versões erradas e confundir usuários/desenvolvedores

**Mitigação sugerida:** centralizar versão em um único módulo (ex.: `src/core/config.py`) e propagar para todos os pontos.

### Monitoramento de RAM pode falhar silenciosamente
- `psutil` é import opcional em `game_controller.py`
- Se não estiver instalado, alerta de RAM não dispara
- Multi-boxing continua sem proteção de memória, sem aviso ao usuário

**Mitigação sugerida:** declarar `psutil` como dependência obrigatória ou exibir aviso na UI quando indisponível.

### Flash Player descontinuado (Adobe EOL 2020)
- Dependência de `pepflashplayer.dll` — plugin sem patches de segurança
- Risco inerente ao ecossistema; mitigado parcialmente por flags Chromium, mas não eliminado

**Mitigação sugerida:** documentar limitação; isolar o launcher; evitar navegação fora do domínio do jogo.

### Permissões Flash injetadas via binário fixo
- `ensure_flash_permissions()` escreve `settings.sol` com payload hardcoded
- Pode conflitar com configurações legítimas do usuário ou falhar em formatos futuros do arquivo

**Mitigação sugerida:** só escrever se arquivo inexistente; fazer backup antes de sobrescrever.

---

## Baixos / técnicos

### `resizeEvent` duplicado em `game_view.py`
- Segunda definição (zoom debounce) sobrescreve a primeira (overlay de loading)
- Overlay pode não redimensionar corretamente ao redimensionar a janela

**Mitigação sugerida:** unificar os dois handlers em um único `resizeEvent`.

### Log referenciado incorretamente no feedback
- `FeedbackService` busca `app.log` em `%LOCALAPPDATA%/LegendOnlineLauncher/logs/`
- Logger grava em `launcher.log` na raiz de `LegendOnlineLauncher`
- Anexo de logs no feedback pode vir vazio mesmo com logs existentes

**Mitigação sugerida:** alinhar caminho e nome do arquivo com `src/core/logger.py`.

### Documentação desatualizada ou quebrada
- `README.md` cita `docs/ANALISE_DO_PROJETO.md`, que não existe
- Instruções de release apontam para executável v2.2, enquanto o projeto está em v2.4.1+

**Mitigação sugerida:** atualizar README e links de documentação.

### Submodule `tools/inspector`
- Proxy global Windows (WinINet) pode afetar todo o sistema
- Risco operacional se o inspector fechar de forma inesperada sem desativar o proxy

**Mitigação sugerida:** garantir cleanup no `closeEvent` (já implementado); documentar uso seguro.

### Dependências sem `requirements.txt`
- PyQt5, psutil, PyInstaller etc. não estão pinados formalmente
- Builds e ambientes de dev podem divergir silenciosamente

**Mitigação sugerida:** adicionar `requirements.txt` ou `pyproject.toml` com versões mínimas testadas.

---

## Matriz de impacto

| Risco | Impacto | Probabilidade |
|-------|---------|---------------|
| Webhook Discord exposto | Abuso do canal / spam | Alta (repo público) |
| Senhas em texto plano | Comprometimento local de contas | Média |
| Proxy cache não wired | Performance abaixo do esperado | Certa (já ocorre) |
| Código legado duplicado | Bugs regressivos | Média |
| Persistência dupla de contas | Perda/dessinc de dados | Baixa–média |
| Flash EOL | Vulnerabilidades não corrigíveis | Alta (longo prazo) |
| Versões inconsistentes | Updates/confusão de release | Média |

---

## Priorização sugerida

1. Rotacionar webhook Discord e externalizar URL
2. Decidir: conectar ou remover `CacheProxyServer`
3. Remover código legado (`launcher_hub.py`, `game_window.py`)
4. Unificar persistência de contas via `AccountService`
5. Centralizar versão do app
6. Corrigir caminho do log no `FeedbackService`
7. Adicionar `requirements.txt`
