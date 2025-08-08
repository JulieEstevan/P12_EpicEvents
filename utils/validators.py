import re


def validate_email(address, field_name="email", max_length=120):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
        raise ValueError("Invalid email format")
    if len(address) > max_length:
        raise ValueError(f"{field_name} address is too long, maximum length is {max_length} characters")
    return address


def validate_string_length(value, field_name, max_length):
    if len(value) > max_length:
        raise ValueError(
            f"{field_name} is too long, maximum length is {max_length} characters"
        )
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty")
    return value


def validate_phone_number(number, field_name="phone", max_length=20):
    if len(number) > max_length:
        raise ValueError(f"{field_name} number is too long, maximum length is {max_length} characters")
    if not re.match(r"^\+?[0-9\s\-()]+$", number):
        raise ValueError("Invalid phone number format")
    return number


def validate_positive_amount(value, field_name, number=0):
    if int(value) < number:
        raise ValueError(f"{field_name} amount must be a positive")
    return value


def validate_positive_integer(value, field_name, number=0):
    if int(value) < number:
        raise ValueError(f"{field_name} value must be a positive")
    return value