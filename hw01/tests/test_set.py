import pytest


class TestSet:

    @pytest.mark.parametrize("sett, length", [
        (set(), 0),
        ({None}, 1),
        ({1, 2, 3}, 3),
    ])
    def test_len(self, sett, length):
        assert len(sett) == length

    @pytest.mark.parametrize("sett, element, has_element", [
        (set(), None, False),
        ({None}, None, True),
        ({2, 3}, 1, False),
        ({2, 3}, 2, True),
    ])
    def test_has_element(self, sett, element, has_element):
        assert (element in sett) == has_element

    @pytest.mark.parametrize("sett, value, result", [
        (set(), 1, {1}),
        ({1}, 1, {1}),
        ({1}, 2, {1, 2}),
    ])
    def test_add(self, sett, value, result):
        sett.add(value)
        assert sett == result

    @pytest.mark.parametrize("sett, value, result", [
        ({1}, 1, set()),
        ({1, 2}, 2, {1}),
    ])
    def test_remove(self, sett, value, result):
        sett.remove(value)
        assert sett == result

    @pytest.mark.parametrize("sett, value", [
        (set({}), 1),
        ({1, 2}, 3),
    ])
    def test_remove_exception(self, sett, value):
        with pytest.raises(KeyError):
            sett.remove(value)
