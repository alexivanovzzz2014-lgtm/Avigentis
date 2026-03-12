from abc import ABC, abstractmethod


class EmailProvider(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None:
        raise NotImplementedError


class MockEmailProvider(EmailProvider):
    def send(self, to: str, subject: str, body: str) -> None:
        print(f'[MOCK EMAIL] to={to} subject={subject} body_length={len(body)}')
