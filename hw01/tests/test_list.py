import pytest


class TestList:

    @pytest.mark.parametrize("lst, length", [
        ([], 0),
        ([None], 1),
        ([1, 2, 3], 3),
    ])
    def test_len(self, lst, length):
        assert len(lst) == length

    @pytest.mark.parametrize("lst, index, element", [
        ([1], 0, 1),
        ([1, 2, 3], 0, 1),
        ([1, 2, 3], 2, 3),
        ([1, 2, 3], -1, 3),
        ([1, 2, 3], -3, 1),
    ])
    def test_indexing(self, lst, index, element):
        assert lst[index] == element

    @pytest.mark.parametrize("lst,index", [
        ([], 0),
        ([], -1),
        ([1, 2, 3], 3),
        ([1, 2, 3], -4),
    ])
    def test_indexing_exception(self, lst, index):
        with pytest.raises(IndexError):
            lst[index]

    @pytest.mark.parametrize("lst, ntimes, result", [
        ([1], 0, []),
        ([1], -1, []),
        ([1], 3, [1, 1, 1]),
    ])
    def test_multiply(self, lst, ntimes, result):
        assert lst * ntimes == result

    @pytest.mark.parametrize("list, slice_from, slice_to, result", [
        ([], 0, -1, []),
        ([1, 2, 3], 0, -1, [1, 2]),
        ([1, 2, 3], 0, 2, [1, 2]),
        ([1, 2, 3], 0, None, [1, 2, 3]),
    ])
    def test_slice(self, list, slice_from, slice_to, result):
        assert list[slice_from:slice_to] == result

    @pytest.mark.parametrize("lst, element, index", [
        ([1, 2, 3, 4], 3, 2),
    ])
    def test_index(self, lst, element, index):
        assert lst.index(element) == index

    @pytest.mark.parametrize("lst, element", [
        ([1, 2, 4], 3),
        ([], 3),
    ])
    def test_index_exceptions(self, lst, element):
        with pytest.raises(ValueError):
            lst.index(element)

    @pytest.mark.parametrize("lst, index, value, result", [
        ([], 0, "value", ["value"]),
        ([1, 2, 3], 0, "value", ["value", 1, 2, 3]),
        ([1, 2, 3], 2, "value", [1, 2, "value", 3]),
        ([1, 2, 3], 3, "value", [1, 2, 3, "value"]),
    ])
    def test_insert(self, lst, index, value, result):
        lst.insert(index, value)
        assert lst == result

    @pytest.mark.parametrize("lst, index, value, result", [
        ([1, 2, 3], 1, 2, [1, 3]),
        ([1], 0, 1, []),
    ])
    def test_pop(self, lst, index, value, result):
        assert lst.pop(index) == value
        assert lst == result

    @pytest.mark.parametrize("lst, value, count", [
        ([], 1, 0),
        ([2, 3], 1, 0),
        ([1, 2, 3], 1, 1),
        ([1, 2, 1, 3, 1], 1, 3),
    ])
    def test_count(self, lst, value, count):
        assert lst.count(value) == count

    @pytest.mark.parametrize("lst, reversed, result", [
        ([], False, []), ([], True, []),
        ([1, 2, 3], False, [1, 2, 3]), ([1, 2, 3], True, [3, 2, 1]),
        ([2, 1, 3], False, [1, 2, 3]), ([2, 1, 3], True, [3, 2, 1]),
    ])
    def test_sort(self, lst, reversed, result):
        lst.sort(reverse=reversed)
        assert lst == result
