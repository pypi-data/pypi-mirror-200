import logging
from enum import StrEnum, auto
from ipaddress import IPv4Address
from typing import TypeAlias

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse, ModbusResponse

from .exceptions import ConfigError, RequestError
from ..models.register import RegisterBase, RegisterInput, RegisterOutput

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


ResponseType: TypeAlias = ExceptionResponse | ModbusResponse
RegistersType: TypeAlias = RegisterBase | RegisterInput | RegisterOutput


class States(StrEnum):
    disconnected = auto()
    connected = auto()


class ModbusClient:
    def __init__(
        self,
        registres: tuple[RegistersType, ...],
        host: IPv4Address,
        port: int = 502,
    ) -> None:
        self.__client: AsyncModbusTcpClient
        self.__state: States
        self.__registers: tuple[RegistersType, ...]

        self.__client = AsyncModbusTcpClient(
            host=str(host),
            port=port,
        )
        self.__state = States.disconnected
        self.__registers = registres

    async def cycle(self):
        await self.__client.connect()
        for address, register in enumerate(self.__registers):
            match register:
                case RegisterInput():
                    await self.__register_write(
                        address=address,
                        value=register.value,
                    )
                case RegisterOutput():
                    register.value = await self.__register_read(
                        address=address,
                    )
                case _:
                    msg = "Неизвестный тип данных регистра: {0}"
                    raise ConfigError(msg.format(type(register)))

    async def __register_write(self, address: int, value: int) -> None:
        try:
            await self.__client.write_register(  # pyright: ignore
                address=address,
                value=value,
            )
        except ModbusException as exc:
            log.error(exc)
            raise ConfigError from exc

    async def __register_read(self, address: int) -> int:
        try:
            rh: ResponseType = (
                await self.__client.read_holding_registers(  # pyright: ignore
                    address=address,
                    count=1,
                )
            )
        except ModbusException as exc:
            log.error(exc)
            raise ConfigError from exc
        _check_modbus_response(rh)
        return rh.registers[0]  # pyright: ignore


def _check_modbus_response(response: ResponseType) -> ModbusResponse:
    """Check modbus call worked generically."""
    match response:
        case ExceptionResponse():
            raise RequestError
        case ModbusResponse():
            return response
