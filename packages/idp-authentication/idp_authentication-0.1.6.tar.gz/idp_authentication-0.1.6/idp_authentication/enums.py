from enum import Enum, EnumMeta


class ChoiceEnumMeta(EnumMeta):
    def __contains__(cls, item: int | str) -> bool:
        if isinstance(item, int):
            member_values = [v.value[0] for v in cls.__members__.values()]
        elif isinstance(item, str):
            item = item.lower()
            member_values = [v.value[1].lower() for v in cls.__members__.values()]
        else:
            member_values = cls.__members__.values()

        return item in member_values


class ChoiceEnum(Enum, metaclass=ChoiceEnumMeta):
    def __str__(self) -> str:
        return self.value[1]

    def __int__(self) -> int:
        return self.value[0]

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        elif isinstance(other, int):
            return int(self) == other
        return self is other

    @classmethod
    def get_by_value(cls, value):
        value_index = 0 if type(value) == int else 1
        return next(
            (v for v in cls.__members__.values() if v.value[value_index] == value), None
        )

    @classmethod
    def list_as(cls, item_type) -> list[int | str]:
        if item_type not in [int, str]:
            raise TypeError("Invalid item type")
        return list(map(item_type, cls))
