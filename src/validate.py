import re


def validate_name(name):
    """
    Validate a person's name.
    """
    if not name:
        return False

    name = name.strip()

    if not name:
        return False

    # Allow letters, spaces, periods and hyphens.
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", name))


def validate_account_number(account_number):
    """
    Validate account number.

    Account numbers are kept as strings so leading zeros
    are preserved.
    """
    if not account_number:
        return False

    account_number = str(account_number).strip()

    # Digits only
    if not account_number.isdigit():
        return False

    # Reasonable banking account-number length.
    return 9 <= len(account_number) <= 18


def validate_ifsc(ifsc_code):
    """
    Validate the basic structural format of an Indian IFSC code.

    Typical structure:
    4 letters + 0 + 6 alphanumeric characters
    Example: HDFC0001234
    """
    if not ifsc_code:
        return False

    ifsc_code = ifsc_code.strip().upper()

    pattern = r"^[A-Z]{4}0[A-Z0-9]{6}$"

    return bool(re.fullmatch(pattern, ifsc_code))


def normalize_amount(amount):
    """
    Convert WhatsApp-style monetary values into numeric rupees.

    Examples:
        12500   -> 12500
        15,500  -> 15500
        25k     -> 25000
        20.5k   -> 20500
    """

    if not amount:
        return None

    value = str(amount).strip().lower()

    # Remove commas
    value = value.replace(",", "")

    # Handle 'k' notation
    if value.endswith("k"):
        number = value[:-1]

        try:
            return float(number) * 1000
        except ValueError:
            return None

    try:
        return float(value)
    except ValueError:
        return None


def normalize_data(extracted_data):
    """
    Convert raw NER output into a clean structured dictionary.
    """

    names = extracted_data.get("NAME", [])
    accounts = extracted_data.get("ACCOUNT_NUMBER", [])
    ifsc_codes = extracted_data.get("IFSC_CODE", [])
    amounts = extracted_data.get("AMOUNT", [])

    name = names[0].strip() if names else None
    account_number = accounts[0].strip() if accounts else None
    ifsc_code = ifsc_codes[0].strip().upper() if ifsc_codes else None
    amount = amounts[0].strip() if amounts else None

    normalized_amount = normalize_amount(amount)

    validation = {
        "name": validate_name(name),
        "account_number": validate_account_number(account_number),
        "ifsc_code": validate_ifsc(ifsc_code),
        "amount": normalized_amount is not None,
    }

    return {
        "name": name,
        "account_number": account_number,
        "ifsc_code": ifsc_code,
        "amount": normalized_amount,
        "validation": validation,
        "is_valid": all(validation.values()),
    }


if __name__ == "__main__":

    sample_data = {
        "NAME": ["Priya Sharma"],
        "ACCOUNT_NUMBER": ["445566778899"],
        "IFSC_CODE": ["hdfc0001234"],
        "AMOUNT": ["15,500"],
    }

    result = normalize_data(sample_data)

    print("=" * 60)
    print("Validation & Normalization")
    print("=" * 60)

    print(result)