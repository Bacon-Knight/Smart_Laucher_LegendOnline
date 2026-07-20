import logging
import os
import sys

def mask_email(email: str) -> str:
    """Anonimiza o e-mail para exibição segura em logs (ex: er***01@gmail.com)."""
    if not email or "@" not in email:
        return email or "Desconhecido"
    name, domain = email.split("@", 1)
    if len(name) <= 2:
        masked = name[0] + "*"
    else:
        masked = name[0] + "*" * (len(name) - 2) + name[-1]
    return f"{masked}@{domain}"

def get_logger(name: str = "Launcher") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler (in AppData)
        app_data_path = os.getenv('LOCALAPPDATA') or os.path.expanduser('~')
        log_dir = os.path.join(app_data_path, "LegendOnlineLauncher")
        os.makedirs(log_dir, exist_ok=True)
        
        from logging.handlers import RotatingFileHandler
        fh = RotatingFileHandler(os.path.join(log_dir, "launcher.log"), maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
        
def setup_global_exception_handler() -> None:
    """Captura qualquer exceção não tratada na aplicação e registra no log com um código de erro."""
    logger = get_logger("GlobalErrorHandler")

    def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # Mapeamento de Códigos de Erro Estruturados
        if issubclass(exc_type, RuntimeError) and "deleted" in str(exc_value).lower():
            error_code = "ERR-QT-501"  # Objeto C++ do Qt/WebEngine deletado prematuramente
        elif issubclass(exc_type, (ConnectionError, TimeoutError)):
            error_code = "ERR-NET-400" # Falha de rede/conexão
        elif issubclass(exc_type, MemoryError):
            error_code = "ERR-MEM-500" # Estouro de memória
        elif issubclass(exc_type, AttributeError):
            error_code = "ERR-REF-404" # Referência a atributo nulo/inexistente
        else:
            error_code = "ERR-UNK-999" # Erro genérico/desconhecido

        logger.critical(
            f"[{error_code}] Exceção não tratada: {exc_type.__name__}: {exc_value}",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

        try:
            from PyQt5.QtCore import QSettings
            app_data_path = os.getenv('LOCALAPPDATA') or os.path.expanduser('~')
            log_path = os.path.join(app_data_path, "LegendOnlineLauncher", "launcher.log")
            settings = QSettings("CustomLauncher", "LegendOnline")
            settings.setValue("has_crashed", True)
            settings.setValue("last_crash_log", log_path)
            settings.setValue("last_crash_code", error_code)
        except Exception as err:
            logger.error(f"Falha ao registrar estado de crash no QSettings: {err}")

    sys.excepthook = handle_uncaught_exception



