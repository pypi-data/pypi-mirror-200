from ..devices.device_base import DeviceBase
from ..register import (
    RegisterBase,
    RegisterInput,
    RegisterOutput,
)
from ..signal_bool import SignalBool


class SiemensCPU1212(DeviceBase):
    def __init__(self) -> None:
        self.__reg_di_a = RegisterInput()
        self.__reg_dq_a = RegisterOutput()
        self.__reg_ai_0 = RegisterInput()
        self.__reg_ai_1 = RegisterInput()

        self.__di_a_0 = SignalBool(self.__reg_di_a, 0)
        self.__di_a_1 = SignalBool(self.__reg_di_a, 1)
        self.__dq_a_0 = SignalBool(self.__reg_dq_a, 8)

    @property
    def registers(self) -> tuple[RegisterBase, ...]:
        return (
            self.__reg_di_a,
            self.__reg_dq_a,
            self.__reg_ai_0,
            self.__reg_ai_1,
        )

    @property
    def di_a_0(self) -> SignalBool:
        return self.__di_a_0

    @property
    def di_a_1(self) -> SignalBool:
        return self.__di_a_1

    @property
    def dq_a_0(self) -> SignalBool:
        return self.__dq_a_0
