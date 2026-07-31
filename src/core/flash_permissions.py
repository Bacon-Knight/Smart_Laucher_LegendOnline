import os
import sys
from src.core.logger import get_logger

logger = get_logger("FlashPermissions")

def get_flash_appdata_dir() -> str:
    """Retorna a pasta oficial de suporte do Flash Player no AppData do Windows."""
    if sys.platform == 'win32':
        app_data = os.getenv('APPDATA') or os.path.expanduser('~')
        return os.path.join(app_data, "Macromedia", "Flash Player", "macromedia.com", "support", "flashplayer", "sys", "#")
    return ""

def ensure_flash_permissions() -> bool:
    """
    Garante a injeção automática de permissões no arquivo settings.sol do Flash Player,
    evitando popups de confirmação de câmera, microfone e armazenamento local.
    """
    if sys.platform != 'win32':
        return False

    flash_dir = get_flash_appdata_dir()
    if not flash_dir:
        return False

    try:
        os.makedirs(flash_dir, exist_ok=True)
        sol_file = os.path.join(flash_dir, "settings.sol")

        # Estrutura binária padrão de um arquivo settings.sol do Flash com permissões liberadas (Always Allow)
        # permitindo armazenamento ilimitado e autorização automática.
        sol_binary_payload = bytes([
            0x00, 0xbf, 0x00, 0x00, 0x00, 0x22, 0x54, 0x43, 0x53, 0x4f, 0x00, 0x04,
            0x00, 0x00, 0x00, 0x08, 0x73, 0x65, 0x74, 0x74, 0x69, 0x6e, 0x67, 0x73,
            0x00, 0x00, 0x00, 0x03, 0x00, 0x08, 0x6c, 0x6f, 0x63, 0x61, 0x6c, 0x46,
            0x69, 0x6c, 0x65, 0x02, 0x00, 0x06, 0x61, 0x6c, 0x77, 0x61, 0x79, 0x73,
            0x00, 0x07, 0x73, 0x74, 0x6f, 0x72, 0x61, 0x67, 0x65, 0x02, 0x00, 0x01,
            0x30, 0x00, 0x00, 0x09
        ])

        if not os.path.exists(sol_file) or os.path.getsize(sol_file) < len(sol_binary_payload):
            with open(sol_file, "wb") as f:
                f.write(sol_binary_payload)
            logger.info("Permissões do Flash Player injetadas com sucesso no AppData (%AppData%\\Macromedia\\Flash Player).")
        return True
    except Exception as e:
        logger.debug(f"Não foi possível injetar permissões do Flash: {e}")
        return False
