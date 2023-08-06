from abc import abstractmethod, ABC


class NuBankServiceBasicInterface(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def authenticate(self,
                     token: str,
                     certificate_path: str):
        pass

    @abstractmethod
    def has_certificate(self, certificate_path: str):
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @abstractmethod
    def get_transactions(self):
        pass


class NuBankServiceInterface:
    def __init__(self,
                 token: str,
                 certificate_path: str,
                 bank_service):
        self.token = token
        self.certificate_path = certificate_path
        self.bank_service = bank_service
        self.has_certificate = self.bank_service.has_certificate(self.certificate_path)

        if self.has_certificate:
            self.bank_service.authenticate(
                self.token,
                self.certificate_path
            )

    def get_balance(self):
        if self.has_certificate:
            return self.bank_service.get_balance()
        return 0

    def get_transactions(self, quantity: None):
        if self.has_certificate:
            transactions = self.bank_service.get_transactions()
            return transactions[:quantity]
        return []
