"""Simple unit converter with a few categories.

Supported categories:
 - length: m, cm, mm, km, in, ft
 - temperature: C, F, K

Extend the dicts to add more units/categories.
"""
from __future__ import annotations
from typing import Dict
from math import isfinite

# Base factors relative to meter
_LENGTH_FACTORS: Dict[str, float] = {
    "m": 1.0,
    "cm": 0.01,
    "mm": 0.001,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
}

_TEMPERATURE_UNITS = {"c", "f", "k"}

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    fu = from_unit.lower()
    tu = to_unit.lower()
    if fu not in _LENGTH_FACTORS:
        raise ValueError(f"Unsupported length unit: {from_unit}")
    if tu not in _LENGTH_FACTORS:
        raise ValueError(f"Unsupported length unit: {to_unit}")
    meters = value * _LENGTH_FACTORS[fu]
    return meters / _LENGTH_FACTORS[tu]

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    fu = from_unit.lower()
    tu = to_unit.lower()
    if fu not in _TEMPERATURE_UNITS:
        raise ValueError(f"Unsupported temperature unit: {from_unit}")
    if tu not in _TEMPERATURE_UNITS:
        raise ValueError(f"Unsupported temperature unit: {to_unit}")

    # normalize to Celsius
    if fu == "c":
        c = value
    elif fu == "f":
        c = (value - 32.0) * 5.0 / 9.0
    else:  # fu == "k"
        c = value - 273.15

    if tu == "c":
        return c
    if tu == "f":
        return c * 9.0 / 5.0 + 32.0
    # tu == "k"
    return c + 273.15

def convert(category: str, value: float, from_unit: str, to_unit: str) -> float:
    """Convert `value` from `from_unit` to `to_unit` within `category`.

    Raises ValueError on unsupported category/units or invalid numeric value.
    """
    if not isfinite(value):
        raise ValueError("Value must be a finite number")
    cat = category.strip().lower()
    if cat == "length":
        return convert_length(value, from_unit, to_unit)
    if cat in ("temperature", "temp", "temperature-celsius"):
        return convert_temperature(value, from_unit, to_unit)
    raise ValueError(f"Unsupported conversion category: {category}")
