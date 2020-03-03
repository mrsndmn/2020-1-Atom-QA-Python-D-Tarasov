import pytest


class TestDict:

    @pytest.mark.parametrize("dictt, length", [
        (dict(), 0),
        ({None: None}, 1),
        ({1: 1, 2: 2, 3: 3}, 3),
    ])
    def test_len(self, dictt, length):
        assert len(dictt) == length

    @pytest.mark.parametrize("dictt, element, has_element", [
        (dict(), None, False),
        ({None: None}, None, True),
        ({2: 2, 3: 3}, 1, False),
        ({2: 2, 3: 3}, 2, True),
    ])
    def test_has_element(self, dictt, element, has_element):
        assert (element in dictt) == has_element

    @pytest.mark.parametrize("dictt, key, value, result", [
        (dict(), 1, 1, {1: 1}),
        ({1: 1}, 1, 1, {1: 1}),
        ({1: 1}, 2, 2, {1: 1, 2: 2}),
    ])
    def test_add(self, dictt, key, value, result):
        dictt[key] = value
        assert dictt[key] == value

    @pytest.mark.parametrize("dictt, key, result", [
        ({1: 1, 2: 2}, 2, {1: 1}),
    ])
    def test_remove(self, dictt, key, result):
        del dictt[key]
        assert key not in dictt
        assert dictt == result

    @pytest.mark.parametrize("dictt, key", [
        (dict({}), 1),
        ({1: 1, 2: 2}, 3),
    ])
    def test_remove_exception(self, dictt, key):
        with pytest.raises(KeyError):
            del dictt[key]
