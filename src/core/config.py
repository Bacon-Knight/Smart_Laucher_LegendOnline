import os
import sys

def resource_path(relative_path):
    """ Pega o caminho absoluto, funcionando tanto em dev quanto num .exe do PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_app_data_dir():
    if sys.platform == 'win32':
        app_data_path = os.getenv('LOCALAPPDATA') or os.path.expanduser('~')
    else:
        app_data_path = os.getenv('XDG_DATA_HOME') or os.path.join(os.path.expanduser('~'), '.local', 'share')
    return os.path.join(app_data_path, "LegendOnlineLauncher")

def get_cache_dir(safe_email):
    return os.path.join(get_app_data_dir(), "cache", safe_email)

def get_shared_cache_dir():
    return os.path.join(get_app_data_dir(), "cache", "shared_assets")

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
