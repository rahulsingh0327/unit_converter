from mcp.server.fastmcp import FastMCP

mcp = FastMCP("UtilityTools")

# -------------------------------------------------------------------
# Conversion Tables & Helper Logic (fully documented)
# -------------------------------------------------------------------

_LENGTH = {
    "m": 1.0, "cm": 0.01, "mm": 0.001, "km": 1000,
    "in": 0.0254, "ft": 0.3048, "yd": 0.9144
}


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a length value between supported units.

    Supported units:
        - Metric: m, cm, mm, km
        - Imperial: in, ft, yd

    The conversion uses a simple factor mapping table.

    Args:
        value (float): The number representing the magnitude.
        from_unit (str): Unit of the input value.
        to_unit (str): Unit to convert into.

    Returns:
        float: Converted length value.
    """
    return (value * _LENGTH[from_unit]) / _LENGTH[to_unit]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert temperature values between Celsius, Fahrenheit and Kelvin.

    Supported transitions:
        - °C ↔ °F
        - °C ↔ K
        - °F ↔ K

    Args:
        value (float): Temperature value.
        from_unit (str): Input temperature scale.
        to_unit (str): Output temperature scale.

    Returns:
        float: Converted temperature.
    """
    fu, tu = from_unit.lower(), to_unit.lower()

    if fu == "c": c = value
    elif fu == "f": c = (value - 32) * 5/9
    elif fu == "k": c = value - 273.15
    else: raise ValueError("Unsupported source temperature unit.")

    if tu == "c": return c
    if tu == "f": return c * 9/5 + 32
    if tu == "k": return c + 273.15

    raise ValueError("Unsupported target temperature unit.")


# -------------------------------------------------------------------
# MCP Tool
# -------------------------------------------------------------------

@mcp.tool()
def unit_converter(category: str, value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert units across categories like length and temperature.

    Supported:
        Length units → m, cm, mm, km, in, ft, yd
        Temperature → Celsius, Fahrenheit, Kelvin

    Args:
        category (str): One of ["length", "temperature"]
        value (float): Numeric input value to convert.
        from_unit (str): The original unit.
        to_unit (str): The desired unit.

    Returns:
        float: Converted output.

    This tool is useful for:
        - Engineering applications
        - Scientific software
        - UI/UX tools needing standardized measurements
        - Data pipelines requiring normalization of units
    """
    category = category.lower()

    if category == "length":
        return convert_length(value, from_unit.lower(), to_unit.lower())

    if category == "temperature":
        return convert_temperature(value, from_unit, to_unit)

    raise ValueError("Unknown conversion category.")
