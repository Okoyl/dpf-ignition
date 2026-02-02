import urllib


def octal_to_decimal(num: int) -> int:
    """
    Converts an integer interpreted as octal to its decimal equivalent.

    Args:
      num (int): The integer representing an octal number.

    Returns:
      int: The decimal equivalent of the octal number.
    """
    return int(str(num), 8)

# RFC 2397 url encoding


def url_encode(str: str) -> str:
    return "data:text/plain," + urllib.parse.quote(str)
