# 🚀 Arquitetura de Distribuição: Repositório Privado + GitHub Releases + GitHub Pages

Este guia define a estrutura ideal para **proteger 100% do seu código-fonte**, mantendo o desenvolvimento no GitHub, distribuindo os executáveis compilados (`.exe`) via **GitHub Releases** e hospedando o site público do projeto via **GitHub Pages**.

---

## 🏛️ 1. Visão Geral da Estrutura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    REPOSITÓRIO PRINCIPAL (PRIVADO)                      │
│ 🔒 Contém o código-fonte Python (.py), lógica do launcher, testes e   │
│    agentes. Apenas VOCÊ tem acesso. Ninguém vê o código!               │
└────────────────────┬────────────────────────────────────────────────────┘
                     │
                     ├────────────────────────────────────────┐
                     ▼                                        ▼
┌──────────────────────────────────────────┐ ┌──────────────────────────────┐
│        GITHUB RELEASES (PÚBLICO)         │ │   GITHUB PAGES (LANDING PAGE)│
│ 📦 Distribuição dos binários compilados │ │ 🌐 Site moderno do launcher │
│    (.exe) gerados pelo Nuitka.           │ │    hospedado gratuitamente.  │
└──────────────────────────────────────────┘ └──────────────────────────────┘
```

---

## 🔒 2. Como Configurar o Repositório Privado (Código-Fonte)

1. No GitHub, crie o repositório do seu projeto marcado como **PRIVATE** (Privado).
2. Todo o desenvolvimento do código em Python (`main.py`, módulos, etc.) ocorre dentro deste repositório.
3. Como ele é privado, o código-fonte jamais será visível para o público geral.

---

## 📦 3. Como Gerar e Publicar as Releases (`.exe`)

Quando você concluir uma nova versão do launcher:

### Passo 1: Compilar o Executável Naitivo
Utilize o **Nuitka** para gerar um binário `.exe` único e ultrarrápido:
```bash
nuitka --standalone --onefile --plugin-enable=pyside6 --windows-disable-console --windows-icon-from-ico=assets/icon.ico --output-dir=dist main.py
```

### Passo 2: Criar a Release no GitHub
1. Vá até a página do seu repositório no GitHub.
2. No menu direito, clique em **Releases** ➔ **Draft a new release**.
3. Escolha uma tag de versão (ex: `v2.4.0`).
4. Adicione o título e as notas de atualização (*Release Notes*).
5. Na área **Attach binaries by dropping them here**, faça o upload do arquivo `main.exe` (renomeado para `BKLauncherLO_v2.4.0.exe`).
6. Clique em **Publish Release**.

---

## 🌐 4. Como Configurar a Landing Page no GitHub Pages

Para ter o site do launcher no ar (usando os arquivos de `docs/index.html`):

### Opção A: Repositório Público para a Landing Page (`bklauncherlo.github.io`)
1. Crie um segundo repositório **PÚBLICO** chamado `bklauncherlo.github.io` ou `BKLauncherLO-Site`.
2. Coloque os arquivos de site da pasta `docs/` (`index.html`, `style.css`, imagens).
3. Ative o **GitHub Pages** nas configurações do repositório (`Settings` ➔ `Pages` ➔ `Source: main branch`).
4. Seu site estará no ar gratuitamente na URL:  
   `https://seu-usuario.github.io/bklauncherlo`

### Opção B: Botão de Download Automático no Site
No arquivo `index.html` da Landing Page, configure o botão **"Baixar Agora"** para sempre puxar o arquivo `.exe` mais recente automaticamente:

```html
<a href="https://github.com/SEU_USUARIO/REPOSITORIO/releases/latest/download/BKLauncherLO_Setup.exe" class="btn-download">
  🚀 Baixar BKLauncherLO (.exe)
</a>
```

---

## 🔄 5. Auto-Updater: Atualização Automática no Launcher

No próprio código do Launcher, você pode consultar a API pública das GitHub Releases para avisar ao usuário quando houver uma nova versão sem precisar expor o código-fonte:

```python
import requests

def verificar_atualizacao(versao_atual="2.4.0"):
    url_api = "https://api.github.com/repos/SEU_USUARIO/REPOSITORIO/releases/latest"
    try:
        response = requests.get(url_api, timeout=5)
        if response.status_code == 200:
            data = response.json()
            versao_remota = data["tag_name"].replace("v", "")
            if versao_remota > versao_atual:
                print(f"🔔 Nova versão disponível: {versao_remota}!")
                link_download = data["assets"][0]["browser_download_url"]
                return link_download
    except Exception:
        pass
    return None
```
