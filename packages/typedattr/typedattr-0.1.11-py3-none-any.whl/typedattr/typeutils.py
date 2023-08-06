"""Useful types"""
from pathlib import Path
from typing import Union, Any, Type

from attrs import AttrsInstance

PathType = Union[Path, str]
TensorType = Any
AttrsClass = Type[AttrsInstance]
