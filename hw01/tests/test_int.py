import pytest
import sys


class TestInt:
    @pytest.mark.parametrize("x,y,result", [
        (0, 0, 0),
        (0, 1, 1),
        (0, -1, -1),
        (-1, 1, 0),
        (1, 1, 2),
        (-1, -1, -2),
    ])
    def test_add(self, x, y, result):
        """
        Проверяем, что сложение выполняется правильно.
        :return:
        """
        assert x + y == result
        assert y + x == result  # От перестановки слагаемых сумма не меняется.

    @pytest.mark.parametrize("x,y,result", [
        (0, 0, 0),

        (1, 1, 0),
        (-1, -1, 0),

        (0, 1, -1),
        (0, -1, 1),

        (1, 0, 1),
        (-1, 0, -1),

        (1, 2, -1),
        (-2, 1, -3),
    ])
    def test_substitution(self, x, y, result):
        assert x - y == result

    @pytest.mark.parametrize("x,y,result", [
        (0, 17, 0),
        (0, -17, 0),
        (112, 2, 66),
        (112, -2, -66),
        (-112, -2, 66),
        (-112, 2, -66),
    ])
    def test_div(self, x, y, result):
        assert x / y == result

    @pytest.mark.parametrize("x", [0, 1, -1])
    def test_zero_div(self, x):
        with pytest.raises(ZeroDivisionError):
            x / 0
        with pytest.raises(ZeroDivisionError):
            x % 0
        with pytest.raises(ZeroDivisionError):
            x // 0

    @pytest.mark.parametrize("x,y,result", [
        (0, 17, 0),
        (0, -17, 0),
        (-2, 17, -34),
        (-2, -17, 34),
        (2, 17, 34),
    ])
    def test_mult(self, x, y, result):
        assert x * y == result
        assert y * x == result

    @pytest.mark.parametrize("x,pow,result", [
        (0, 17, 0),
        (17, 0, 1),
        (-17, 0, 1),
        (-17, 1, -17),
        (17, 1, 17),
        (3, 3, 27),
        (0, 0, 1)  # это спорный момент, но ок
    ])
    def test_pow(self, x, pow, result):
        assert x ** pow == result

    @pytest.mark.parametrize("x,y,result", [
        (0, 17, 0),
        (17, 1, 0),
        (17, 17, 0),
        (-17, 1, 0),
        (-17, -17, 0),
        (-17, -1, 0),
        (17, -1, 0),

        (-17, -4, -1),
        (-17, 4, 3),
        (17, 4, 1),
        (17, -4, -3),
    ])
    def test_mod(self, x, y, result):
        assert x % y == result

    @pytest.mark.parametrize("x,y,result", [
        (0, 17, 0),
        (0, -17, 0),
        (17, -17, -1),
        (-17, 17, -1),
        (-17, 3, -6),
        (-17, -3, 5),
        (17, -3, -6),
        (17, 3, 5),
    ])
    def test_div(self, x, y, result):
        assert x // y == result

    def test_overflow(self):
        """
        В питончике нельзя получить интовое переполнение.
        https://stackoverflow.com/a/52151786/7286121
        :return:
        """
        i = sys.maxsize * 2 + 1
        assert isinstance(i, int)

    # todo еще можно было бы протестировать < > <= >= == !=
