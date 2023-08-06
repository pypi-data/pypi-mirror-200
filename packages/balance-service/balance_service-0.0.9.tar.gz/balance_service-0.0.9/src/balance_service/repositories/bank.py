from abc import abstractmethod, ABC

from balance_domain.entities.bank import BankEntity


class BankRepositorie(ABC):
    @abstractmethod
    def create(self, user: BankEntity):
        pass

    @abstractmethod
    def get_by_id(self, bank_id: int):
        pass

    def get_by_user_id(self, user_id: int):
        pass
