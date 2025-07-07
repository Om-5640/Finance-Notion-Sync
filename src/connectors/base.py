import abc

class Connector(abc.ABC):
    @abc.abstractmethod
    def fetch_transactions(self, since_timestamp: str) -> list:
        """Return a list of transactions newer than the ISO timestamp."""
        pass
