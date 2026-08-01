import os
import json
import urllib.request
import urllib.error
from src.core.logger import get_logger

logger = get_logger("FeedbackService")

class FeedbackService:
    """
    Serviço assíncrono para envio de relatórios de bugs e sugestões
    através do Gateway Seguro Vercel (protegendo o webhook do Discord).
    """
    
    # URL da Serverless Function na Vercel (pode ser sobrescrita via variável de ambiente FEEDBACK_PROXY_URL)
    DEFAULT_PROXY_URL = os.getenv("FEEDBACK_PROXY_URL", "https://smart-laucher-legend-online.vercel.app/api/feedback")

    @staticmethod
    def send_feedback(category: str, message: str, user_contact: str = "", include_logs: bool = False, proxy_url: str = None) -> tuple:
        target_url = proxy_url or FeedbackService.DEFAULT_PROXY_URL
        if not target_url:
            logger.warning("Feedback não enviado: URL da Vercel/Proxy não configurada.")
            return False, "NO_WEBHOOK"
        
        log_snippet = ""
        if include_logs:
            try:
                base_dir = os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser('~'), "LegendOnlineLauncher")
                candidate_paths = [
                    os.path.join(base_dir, "launcher.log"),
                    os.path.join(base_dir, "logs", "launcher.log"),
                    os.path.join(base_dir, "logs", "app.log")
                ]
                log_path = next((p for p in candidate_paths if os.path.exists(p)), None)
                if log_path:
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()[-30:]
                        log_snippet = "".join(lines)
            except Exception as e:
                logger.debug(f"Não foi possível anexar trecho do log: {e}")

        payload = {
            "category": category,
            "message": message,
            "user_contact": user_contact or "Anônimo",
            "include_logs": include_logs,
            "log_snippet": log_snippet
        }

        app_secret = os.getenv("APP_CLIENT_SECRET", "BK_LAUNCHER_SECRET_2026")
        
        try:
            req = urllib.request.Request(
                target_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "BKLauncherFeedback/2.4.3",
                    "X-App-Secret": app_secret
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                if resp.status in (200, 204):
                    logger.info("Feedback enviado com sucesso via Gateway Vercel.")
                    return True, "SUCCESS"
        except Exception as e:
            logger.warning(f"Não foi possível enviar feedback via Vercel Proxy: {e}")
        
        return False, "NETWORK_ERROR"
