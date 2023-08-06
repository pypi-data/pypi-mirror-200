import os
from typing import Tuple, Optional, Mapping


def example_module() -> str:
    return "example_module"


class Helper:
    def __init__(self, path: str) -> None:
        self.path = path
        self.details: Mapping[str, str] = {
            "author": "Jane Doe",
            "email": "jane_doe@example.com",
            "project_name": "hello_world",
        }

    def get_path(self) -> str:
        return os.path.join(os.getcwd(), self.path)

    def set_details(self, author: str, email: str, project_name: str) -> None:
        self.details["author"] = author
        self.details["email"] = email
        self.details["project_name"] = project_name

    def check_email(self) -> bool:
        return "@" in self.details["email"]

    def check_project_name(self) -> bool:
        return " " not in self.details["project_name"]

    def valid_details(self) -> bool:
        return self.check_email() and self.check_project_name()


class Worker:
    def __init__(self) -> None:
        self.helper: Helper = Helper("default_path")

    def get_path(self) -> str:
        return self.helper.get_path()


class Field:
    def __init__(self, type_: str, default: str, value: Optional[str] = None) -> None:
        self.type_ = type_
        self.default = default
        self._value = value

    @property
    def value(self) -> str:
        if self._value is None:
            return self.default
        else:
            return self._value


class CountryPricer:
    COUNTRIES: Tuple[str, ...] = ("US", "CN", "JP", "DE", "ES", "FR", "NL")
    DISCOUNT: float = 0.8
    country: Field = Field(type_="str", default=COUNTRIES[0])

    def get_discounted_price(self, price: float, country: str) -> float:
        if country == self.country.value:
            return price * self.DISCOUNT
        else:
            return price
