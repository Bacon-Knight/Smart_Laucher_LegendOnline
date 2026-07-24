import os
import sys

def resource_path(relative_path: str) -> str:
    """ Pega o caminho absoluto, funcionando tanto em dev quanto num .exe do PyInstaller """
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_app_data_dir() -> str:
    if sys.platform == 'win32':
        app_data_path = os.getenv('LOCALAPPDATA') or os.path.expanduser('~')
    else:
        app_data_path = os.getenv('XDG_DATA_HOME') or os.path.join(os.path.expanduser('~'), '.local', 'share')
    return os.path.join(app_data_path, "LegendOnlineLauncher")

def get_cache_dir(safe_email: str) -> str:
    return os.path.join(get_app_data_dir(), "cache", safe_email)

def get_shared_cache_dir() -> str:
    return os.path.join(get_app_data_dir(), "cache", "shared_assets")

def get_login_js_script(email_json: str, password_json: str) -> str:
    """Carrega o script de login a partir do arquivo JS em assets se existir, ou usa a constante fallback."""
    js_path = resource_path(os.path.join("src", "assets", "js", "login.js"))
    if os.path.exists(js_path):
        try:
            with open(js_path, "r", encoding="utf-8") as f:
                content = f.read()
                return content.replace("__EMAIL__", email_json).replace("__PASSWORD__", password_json)
        except Exception:
            pass
    return LOGIN_JS_SCRIPT.format(email_json=email_json, password_json=password_json)

LOGIN_JS_SCRIPT = """
setTimeout(function() {{
    var emailInput = document.querySelector('input[type="email"]') || document.querySelector('input[name="email"]') || document.querySelector('input[name="login"]') || document.querySelector('input[name="account"]') || document.querySelector('input[name="username"]') || document.querySelector('input[type="text"]');
    var passInput = document.querySelector('input[type="password"]') || document.querySelector('input[name="password"]');
    
    if(emailInput && passInput) {{
        emailInput.value = {email_json};
        passInput.value = {password_json};
        
        emailInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        passInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        emailInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        passInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        
        var btn = document.querySelector('button[type="submit"], input[type="submit"], .btn-login, .login-btn, #btnLogin') || document.evaluate("//*[contains(text(), 'Login')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if(btn && typeof btn.click === 'function') {{
            btn.click();
        }} else if (emailInput.form) {{
            emailInput.form.submit();
        }}
        console.log("Credenciais injetadas pelo Custom Launcher!");
    }}

    // Auto-clique em botões de entrada/jogo caso esteja na lista de servidores
    setTimeout(function() {{
        var playBtn = document.querySelector('.btn-play, .play-btn, .btn-enter, #btnPlay, .enter-game, .btn_start') ||
                      document.evaluate("//a[contains(text(), 'Jogar') or contains(text(), 'Entrar') or contains(text(), 'Play')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue ||
                      document.evaluate("//button[contains(text(), 'Jogar') or contains(text(), 'Entrar') or contains(text(), 'Play')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if(playBtn && typeof playBtn.click === 'function') {{
            playBtn.click();
            console.log("Botão de entrada no jogo clicado automaticamente!");
        }}
    }}, 1500);
}}, 1500);
"""


COLOR_MAP = {
    "Vermelho": "#2b0a0a",
    "Azul": "#0a1b2b",
    "Verde": "#0a2b10",
    "Dourado": "#2b250a",
    "Roxo": "#210a2b"
}

BRIGHT_COLORS = {
    "#2b0a0a": "#ff4d4d", 
    "#0a1b2b": "#4d94ff", 
    "#0a2b10": "#4dff88", 
    "#2b250a": "#ffcc00", 
    "#210a2b": "#b366ff", 
    "#120c18": "#cccccc"  
}

COLOR_ORDER = ["Verde", "Azul", "Roxo", "Dourado", "Vermelho"]

GAME_URL_TEMPLATE = "https://lobr.creaction-network.com/serverlist/s{server_num}"
