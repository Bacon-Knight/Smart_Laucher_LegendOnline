# 📊 Análise Comparativa e Oportunidades de Implementação: Launcher Allan vs. BKLauncherLO

Este documento resume a análise técnica realizada sobre o código descompilado do **LegendOnlineClient** (`launcher allan` em C# / .NET 4.8 / CefSharp) e mapeia as diferenças arquiteturais, boas práticas e possíveis implementações a serem integradas no **BKLauncherLO** (Python / PySide6 / QWebEngine).

---

## 🔍 1. Resumo do Launcher Analisado (`launcher allan`)

O **LegendOnlineClient** é um cliente desktop em C# WinForms focado no jogo *Legend Online BR*.

* **Stack:** C# (.NET Framework 4.8, x86), CefSharp (Chromium Web Browser), PPAPI Flash (`pepflashplayer32.dll` v32.0.0.465), Newtonsoft.Json.
* **Foco:** Desempenho leve para jogo em Flash, suporte a múltiplas contas simultâneas, salvamento seguro de credenciais localmente e bloqueio de rastreadores para acelerar navegação.

---

## ⚙️ 2. Mapeamento Técnico de Funcionalidades

### A. Otimização de Desempenho e Recursos do Chromium
* **Prioridade de Processos:** Eleva dinamicamente a prioridade do processo principal e de todos os subprocessos `CefSharp.BrowserSubprocess.exe` para `AboveNormal`.
* **Desativação de Throttling em Segundo Plano:**
  * `--disable-background-timer-throttling=1`
  * `--disable-backgrounding-occluded-windows=1`
  * `--disable-renderer-backgrounding=1`
* **Desativação de Isolamento Rígido de Sites:**
  * `--disable-site-isolation-trials`
  * `--disable-features=IsolateOrigins,site-per-process`
  * *Motivo:* Facilita a injeção JS cross-origin e reduz o consumo excessivo de memória RAM ao abrir múltiplas instâncias.
* **GPU & Acceleration:**
  * `--ignore-gpu-blocklist=1`
  * `--enable-gpu-rasterization=1`
  * `--enable-zero-copy=1`

### B. Proteção e Armazenamento de Contas
* **Criptografia DPAPI (Windows):** Utiliza `System.Security.Cryptography.ProtectedData` com o escopo `DataProtectionScope.CurrentUser`.
* **Mecanismo:** As senhas salvas no arquivo `profiles.json` não ficam em texto puro; são criptografadas com a chave do usuário logado no Windows. Caso o arquivo JSON seja copiado para outro computador, as senhas não podem ser descriptografadas.

### C. Injeção de Login Automático
* **Mapeamento de Eventos:** Intercepta o término do carregamento do iframe de login (`login.creaction-network.com`).
* **Injeção de JS:** Preenche os elementos `#username` e `#password` diretamente no DOM e dispara o evento da função de login `login_button_click()`.

### D. Bloqueio de Rastreadores (AdBlock Embutido)
* Intercepta requisições via `IResourceRequestHandler` e cancela a carga de domínios pesados/rastreadores (`google-analytics.com`, `googletagmanager.com`, `vipsac.oasgames.com`, `collect.mdata.cool`, `pin.oasgames.com`, `oasgames.com`).

---

## ⚔️ 3. Tabela Comparativa de Arquitetura

| Funcionalidade / Aspecto | `launcher allan` (C# / CefSharp) | `BKLauncherLO` (Python / PySide6) |
| :--- | :--- | :--- |
| **Engine Web** | Chromium 80+ via CefSharp | Chromium via QtWebEngine (PySide6) |
| **Arquitetura de UI** | Windows Forms (WinForms) | PySide6 (Qt6 Modern GUI) |
| **Persistência de Senhas** | Windows DPAPI (`ProtectedData`) | Criptografia local / JSON de perfil |
| **Controle de Prioridade OS** | Loop a cada 3s elevando prioridade para `AboveNormal` | Gerenciamento padrão de processos do SO |
| **Interceptação de Requisições** | `IResourceRequestHandler` no CefSharp | `QWebEngineUrlRequestInterceptor` no Qt |
| **Redirecionamento de Pop-ups** | `ILifeSpanHandler` (mesmo host redireciona na aba principal) | Gerenciador de abas / `createWindow` no QWebEngineView |

---

## 💡 4. Sugestões de Implementações Futuras para o `BKLauncherLO`

As seguintes funcionalidades foram identificadas no `launcher allan` e podem ser portadas ou adaptadas para o `BKLauncherLO`:

### 📥 1. Adicionar Flags de Desempenho do Chromium (Prioridade: Média)
* **Objetivo:** Impedir congelamento de abas em segundo plano quando o usuário joga com múltiplas contas.
* **Implementação:** Passar argumentos como `--disable-background-timer-throttling` e `--disable-renderer-backgrounding` na inicialização do `QCoreApplication` / `QWebEngine`.

### 🛡️ 2. Utilizar Criptografia DPAPI no Windows via Python (`pywin32` / `ctypes`) (Prioridade: Alta)
* **Objetivo:** Elevar o nível de segurança do armazenamento de contas no Windows sem exigir senhas mestras.
* **Implementação:** Criptografar as senhas das contas com DPAPI (`crypt32.dll` via `ctypes` ou `win32crypt`) antes de salvar no JSON do `BKLauncherLO`.

### ⚡ 3. Otimização de Prioridade de Processo (Prioridade: Baixa/Média)
* **Objetivo:** Dar prioridade de CPU para o launcher e processos do WebEngine em máquinas fracas.
* **Implementação:** Usar a biblioteca `psutil` em Python para definir `process.nice(psutil.HIGH_PRIORITY_CLASS)` no Windows.

### 🚫 4. Lista Expansível de Bloqueio de Telemetria (AdBlocker de Lista Negra) (Prioridade: Média)
* **Objetivo:** Reduzir consumo de dados e acelerar carregamento do Legend Online.
* **Implementação:** Expandir o `QWebEngineUrlRequestInterceptor` existente para bloquear domínios como `mdata.cool` e `vipsac.oasgames.com`.

---

> 📝 **Nota:** Este documento serve como referência de engenharia reversa e guia de decisões para evolução do **BKLauncherLO**.
