import abc

from ..register import RegisterBase


class DeviceBase(abc.ABC):
    @property
    @abc.abstractmethod
    def registers(self) -> tuple[RegisterBase, ...]:
        ...
