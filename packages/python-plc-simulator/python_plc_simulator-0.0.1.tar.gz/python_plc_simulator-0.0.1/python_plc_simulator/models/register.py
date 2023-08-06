class RegisterBase:
    def __init__(self) -> None:
        self.__value: int = int()

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: int) -> None:
        self.__value = value


class RegisterInput(RegisterBase):
    pass


class RegisterOutput(RegisterBase):
    pass
