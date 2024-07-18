def parse_currency_to_float(currency: str) -> float:
    """
    Convert a currency string to a float. The currency string can contain commas
    and may end with 'M' for millions or 'B' for billions.

    Args:
        currency (str): The currency string to be converted.

    Returns:
        float: The numeric value of the currency string.

    Examples:
        >>> parse_currency_to_float("1,234.56")
        1234.56
        >>> parse_currency_to_float("2.5M")
        2500000.0
        >>> parse_currency_to_float("3B")
        3000000000.0
    """
    # Remove commas from the currency string
    currency_str = currency.replace(",", "")

    # Check if the last character is 'M' for millions
    if currency_str[-1] == "M":
        # Convert the numeric part to float and multiply by 1,000,000
        return float(currency_str[:-1]) * 1_000_000

    # Check if the last character is 'B' for billions
    elif currency_str[-1] == "B":
        # Convert the numeric part to float and multiply by 1,000,000,000
        return float(currency_str[:-1]) * 1_000_000_000

    # If no suffix, convert the entire string to float
    return float(currency_str)
