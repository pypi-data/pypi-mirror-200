from abc import ABC, abstractmethod


class ComposeUnit(ABC):
    @abstractmethod
    def create(self) -> None:
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def install_requirements(self) -> None:
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError("This is an abstract method!")

    @abstractmethod
    def clean(self) -> None:
        raise NotImplementedError("This is an abstract method!")
