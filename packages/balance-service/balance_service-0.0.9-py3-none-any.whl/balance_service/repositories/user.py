from abc import abstractmethod, ABC

from balance_domain.entities.user import UserEntity


class UserRepositorie(ABC):
    @abstractmethod
    def create(self, user: UserEntity):
        pass

    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    def get_by_email(self, user_email: str):
        pass
