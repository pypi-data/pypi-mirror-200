from __future__ import annotations
from ._relations import DataSet, CSVCompression, SandBox, sandbox, ParquetCodec
from ._cli import cli
from ._api import register, login, forget_me
from ._uom import *
from ._version import version as __version__
from . import apps
from . import svr
from . import functions
from . import _uom


svr.get_service(svr.ITelemetryService).library_loaded()

__all__ = ["__version__", "svr", "apps"]
__all__ += ["cli"]
__all__ += ['DataSet', 'CSVCompression', 'SandBox', 'sandbox', 'ParquetCodec', 'functions']
__all__ += ['register', 'login', 'forget_me']
__all__ += _uom.__all__
