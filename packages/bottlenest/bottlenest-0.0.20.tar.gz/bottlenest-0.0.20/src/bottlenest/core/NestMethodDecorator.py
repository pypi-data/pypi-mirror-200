from abc import ABC
from typing import Callable, Any


class NestMethodDecorator(ABC):
    callback: Callable
