from dataclasses import dataclass, fields

from .register import RegisterBase


@dataclass
class DeviceConfigurationBase(object):
    @property
    def all_registres(self) -> tuple[RegisterBase, ...]:
        devices = (getattr(self, field.name) for field in fields(self))
        registers = (dev.registers for dev in devices)
        return tuple(*registers)
