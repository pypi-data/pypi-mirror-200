# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABC, abstractmethod
from typing import Any

from ..model.function import FunctionProfile
# from ...apps import Widget


class IExecutionService(ABC):
    @abstractmethod
    def execute_function(self, fn: FunctionProfile) -> Any:
        pass
