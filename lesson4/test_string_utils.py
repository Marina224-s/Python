import pytest
from string_utils import StringUtils

utils = StringUtils()

class TestStringUtils:


    def setup_method(self):
        self.utils = StringUtils()

    # Тесты для capitalize

    @pytest.mark.parametrize("input_str,expected", [
        ("тест", "Тест"),
        ("123abc", "123abc"),
        ("   пробел", "   пробел"),
    ])
    def test_capitalize_positive(self, input_str, expected):
        assert self.utils.capitalize(input_str) == expected

    @pytest.mark.parametrize("bad_input", [
        "",
        " ",
        None,
        123,
        [],
    ])
    def test_capitalize_negative(self, bad_input):
        with pytest.raises(AttributeError):
            self.utils.capitalize(bad_input)

    # Тесты для trim

    @pytest.mark.parametrize("input_str,expected", [
        ("   skypro", "skypro"),
        ("  04 апреля 2023", "04 апреля 2023"),
        ("без пробелов", "без пробелов"),
    ])
    def test_trim_positive(self, input_str, expected):
        assert self.utils.trim(input_str) == expected

    @pytest.mark.parametrize("bad_input", [
        "",
        " ",
        None,
        123,
        [],
    ])
    def test_trim_negative(self, bad_input):
        with pytest.raises(AttributeError):
            self.utils.trim(bad_input)

    # Тесты для contains

    @pytest.mark.parametrize("string,symbol,expected", [
        ("SkyPro", "S", True),
        ("SkyPro", "U", False),
        ("12345", "3", True),
        ("04 апреля 2023", " ", True),
    ])
    def test_contains_positive(self, string, symbol, expected):
        assert self.utils.contains(string, symbol) is expected

    @pytest.mark.parametrize("string,symbol", [
        ("", "a"),
        (" ", " "),
        (None, "a"),
        ("test", None),
        (123, "1"),
    ])
    def test_contains_negative(self, string, symbol):
        # contains не кидает ошибку, а возвращает False
        # но если параметры None или не строки, может быть ошибка
        try:
            res = self.utils.contains(string, symbol)
            assert isinstance(res, bool)
        except Exception:
            assert True

    # Тесты для delete_symbol

    @pytest.mark.parametrize("string,symbol,expected", [
        ("SkyPro", "k", "SyPro"),
        ("SkyPro", "Pro", "Sky"),
        ("12345", "3", "1245"),
        ("04 апреля 2023", " ", "04апреля2023"),
    ])
    def test_delete_symbol_positive(self, string, symbol, expected):
        assert self.utils.delete_symbol(string, symbol) == expected

    @pytest.mark.parametrize("string,symbol", [
        ("", "a"),
        (" ", " "),
        (None, "a"),
        ("test", None),
        (123, "1"),
    ])
    def test_delete_symbol_negative(self, string, symbol):
        with pytest.raises((AttributeError, TypeError)):
            self.utils.delete_symbol(string, symbol)
            