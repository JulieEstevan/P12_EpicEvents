import re


def validate_email(address):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
        raise ValueError("Invalid email format")
    if len(address) > 120:
        raise ValueError("Email address is too long, maximum length is 120 characters")
    return address


def validate_string_length(value, field_name, max_length):
    if len(value) > max_length:
        raise ValueError(
            f"{field_name} is too long, maximum length is {max_length} characters"
        )
    return value


def validate_phone_number(number):
    if len(number) > 20:
        raise ValueError("Phone number is too long, maximum length is 20 characters")
    # Ajoutez une validation du format si nécessaire
    return number


def validate_positive_amount(value, field_name):
    if value < 0:
        raise ValueError(f"{field_name} amount must be a positive")
    return value


def validate_positive_integer(value, field_name):
    if value < 0:
        raise ValueError(f"{field_name} value must be a positive")
    return value