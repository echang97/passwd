from secrets import token_urlsafe

from passwd import PasswordRequirements


def test_min_length():
    length_8 = PasswordRequirements(min_length=8)

    assert length_8.check("abcd1234")
    assert not length_8.check("abc123")

    # No minimum characters requirement if not specified
    assert PasswordRequirements().check("abc123")


def test_min_digits():
    digits_2 = PasswordRequirements(min_digits=2)

    assert not digits_2.check("abc")
    assert not digits_2.check("abc1")

    assert digits_2.check("abc12")
    assert digits_2.check("abc123")


def test_special_characters():
    special_1 = PasswordRequirements(min_special=1)

    assert special_1.check("abc$")
    assert special_1.check("abc$%^@*")

    assert not special_1.check("abc")
    assert not special_1.check("abc123")


def test_min_alpha():
    alpha_4 = PasswordRequirements(min_alpha=4)

    assert alpha_4.check("abcd123")
    assert alpha_4.check("aBcD123")

    assert not alpha_4.check("aBc$%^")
    assert not alpha_4.check("aBc123")


def test_min_uppercase():
    upper_3 = PasswordRequirements(min_upper=3)

    assert upper_3.check("ABC")
    assert upper_3.check("ABCD")

    assert not upper_3.check("Abc")
    assert not upper_3.check("ABc")


def test_min_lowercase():
    lower_3 = PasswordRequirements(min_lower=3)

    assert lower_3.check("abc")
    assert lower_3.check("abcd")

    assert not lower_3.check("ABC")
    assert not lower_3.check("abC")


def test_combinations():
    length_6_digits_3 = PasswordRequirements(min_length=6, min_digits=3)

    assert length_6_digits_3.check("abc123")

    assert not length_6_digits_3.check("ab123")
    assert not length_6_digits_3.check("abcd12")
    assert not length_6_digits_3.check("ab12")


def test_custom_func():
    def length_3_8(password):
        return 3 < len(password) < 8

    custom_func = PasswordRequirements(func=length_3_8)

    assert custom_func.check("12345")
    assert not custom_func.check("1")
    assert not custom_func.check("123456789")


def test_check_breaches():
    check_breaches = PasswordRequirements(check_breaches=True)

    exposed_passwords = ["12345", "password", "drowssap", "!@#$%^&*()"]
    for password in exposed_passwords:
        assert not check_breaches.check(password)

    for _ in range(3):
        assert check_breaches.check(token_urlsafe(32))
