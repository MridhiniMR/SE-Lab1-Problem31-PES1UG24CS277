import math
from datetime import date

# Convention used by all three functions: invalid input never raises, the
# function returns None instead. Callers (like main) check for None.


def _is_plain_digits(text):
    """True only for a non-empty run of ASCII digits 0-9.

    str.isdigit() alone also accepts digits from other scripts (e.g. Arabic-Indic
    or full-width digits), and int() accepts things like '+5', ' 7' and '1_0'.
    Requiring ASCII digits rejects all of those surprises.
    """
    return text != "" and text.isascii() and text.isdigit()


def split_code(code):
    """Split a coupon code like 'save-20' into ('SAVE', 20).

    Returns None if the input is not a string or not exactly 'PREFIX-NUMBER'
    with an alphanumeric prefix and a non-negative whole-number value.
    """
    if not isinstance(code, str):
        return None
    parts = code.strip().upper().split('-')
    if len(parts) != 2:
        return None
    prefix, value = parts
    if prefix == "" or not (prefix.isascii() and prefix.isalnum()):
        return None
    if not _is_plain_digits(value):
        return None
    try:
        return prefix, int(value)
    except ValueError:  # e.g. absurdly long digit strings hit Python's int limit
        return None


def most_expensive(prices_csv):
    """Return the highest price in a comma-separated string as a float.

    Returns None if the input is not a string, is empty, has an empty or
    non-numeric item, or contains a negative, NaN or infinite price.
    """
    if not isinstance(prices_csv, str):
        return None
    prices = []
    for item in prices_csv.split(','):
        item = item.strip()
        if item == "" or "_" in item:  # float() would accept '1_0'
            return None
        try:
            price = float(item)
        except ValueError:
            return None
        if not math.isfinite(price) or price < 0:
            return None
        prices.append(price)
    return max(prices)


def expiry_days(date_text):
    """Return days since 2024 (approximate: 365-day years, 30-day months)
    for a 'YYYY-MM-DD' string.

    Returns None if the input is not a string or not a real calendar date.
    """
    if not isinstance(date_text, str):
        return None
    parts = date_text.strip().split('-')
    if len(parts) != 3 or not all(_is_plain_digits(p) for p in parts):
        return None
    try:
        year, month, day = (int(p) for p in parts)
        date(year, month, day)  # rejects month 13, Feb 30, year 0, year > 9999...
    except ValueError:
        return None
    return (year - 2024) * 365 + (month - 1) * 30 + day


def main():
    print("==== Running split_code ====")
    user_input = input("Enter a coupon code (e.g. save-20): ")
    result = split_code(user_input)
    if result is None:
        print("Invalid coupon code. Expected format: PREFIX-NUMBER (e.g. save-20)")
    else:
        print("Prefix and Value:", result)

    print("\n==== Running most_expensive ====")
    user_input = input("Enter item prices as CSV (e.g. 199,49.5,320): ")
    result = most_expensive(user_input)
    if result is None:
        print("Invalid prices. Enter non-negative numbers separated by commas.")
    else:
        print("Most Expensive Item:", result)

    print("\n==== Running expiry_days ====")
    user_input = input("Enter an expiry date as YYYY-MM-DD: ")
    result = expiry_days(user_input)
    if result is None:
        print("Invalid date. Enter a real date as YYYY-MM-DD.")
    else:
        print("Days Since 2024:", result)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
