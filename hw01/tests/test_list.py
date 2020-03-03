import pytest


class TestList:

    def test_len(self, lst, length):
        assert len(lst) == length

    # todo test negative indexes
    def test_indexing(self, lst, index, element):
        assert lst[index] == element

    def test_multiply(self, lst, ntimes, result):
        assert lst * ntimes == result

    def test_slice(self, list, slice_from, slice_to, result):
        assert list[slice_from:slice_to] == result

    def test_index(self, lst, element, index):
        assert lst.index(element) == index

    def test_insert(self, lst: list, index, value, result):
        assert lst.insert(index, value) == result

    def test_pop(self, lst: list, index, value, result):
        assert lst.pop(index) == value
        assert lst == result

    def test_count(self, lst, value, count):
        assert lst.count(value) == count

    def test_sort(self, lst, reversed, result):
        assert lst.sort(reversed=reversed) == result
