import json
from typing import List, Optional
from PyQt5.QtCore import QSettings
from src.models.account import Account
from src.core.logger import get_logger

logger = get_logger("AccountService")

class AccountService:
    """Serviço responsável pelo gerenciamento e persistência das contas salvas no QSettings."""
    
    def __init__(self, organization: str = "CustomLauncher", application: str = "LegendOnline") -> None:
        self.settings = QSettings(organization, application)

    def get_all_accounts(self) -> List[Account]:
        """Carrega e retorna todas as contas cadastradas."""
        try:
            accs_str = self.settings.value("accounts", "[]")
            raw_list = json.loads(accs_str)
            accounts = []
            for item in raw_list:
                if isinstance(item, dict):
                    accounts.append(Account.from_dict(item))
            return accounts
        except Exception as e:
            logger.error(f"Erro ao carregar contas do QSettings: {e}")
            return []

    def save_all_accounts(self, accounts: List[Account]) -> bool:
        """Salva a lista completa de contas no QSettings."""
        try:
            raw_list = [acc.to_dict() for acc in accounts]
            self.settings.setValue("accounts", json.dumps(raw_list))
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar contas no QSettings: {e}")
            return False

    def add_or_update_account(self, account: Account) -> List[Account]:
        """Adiciona uma nova conta ou atualiza se o e-mail já existir."""
        accounts = self.get_all_accounts()
        updated = False
        for i, acc in enumerate(accounts):
            if acc.email.lower() == account.email.lower():
                accounts[i] = account
                updated = True
                break
        if not updated:
            accounts.append(account)
        self.save_all_accounts(accounts)
        return accounts

    def delete_account_by_email(self, email: str) -> List[Account]:
        """Remove uma conta pelo e-mail."""
        accounts = self.get_all_accounts()
        filtered = [acc for acc in accounts if acc.email.lower() != email.lower()]
        self.save_all_accounts(filtered)
        return filtered
