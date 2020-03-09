import pytest


class TestString:

    @pytest.mark.parametrize("a, b, result", [
        ("", "", ""),
        ("", "1", "1"),
        ("1", "", "1"),
        ("ё", "ἱερογλύφος", "ёἱερογλύφος"),
    ])
    def test_concat(self, a, b, result):
        assert a + b == result

    @pytest.mark.parametrize("string, ntimes, result", [
        ("ёёё", 0, ""),
        ("ёёё", -1, ""),
        ("ёёё", 5, "ёёёёёёёёёёёёёёё"),
    ])
    def test_multiply(self, string, ntimes, result):
        assert string * ntimes == result

    @pytest.mark.parametrize("string, substring, result", [
        ("ёёё", "", 0),
        ("ёёё", "_", -1),
        ("", "", 0),
        ("", "_", -1),
        ("ё_ёё", "_", 1),
    ])
    def test_substr(self, string, substring, result):
        assert string.find(substring) == result

    @pytest.mark.parametrize("string, delim, result", [
        ("123", "2", ["1", "3"]),
        ("1", "2", ["1"]),
        ("1", "1", ["", ""]),
    ])
    def test_split(self, string, delim, result):
        assert string.split(delim) == result

    @pytest.mark.parametrize("string, delim", [
        ("", ""),
        ("123", ""),
    ])
    def test_split_exception(self, string, delim):
        with pytest.raises(ValueError):
            string.split(delim)

    @pytest.mark.parametrize("string, striped_string", [
        ("", ""),
        ("   ", ""),
        ("  _  ", "_"),
        ("  _ _  ", "_ _")
    ])
    def test_strip(self, string, striped_string):
        assert string.strip() == striped_string

    @pytest.mark.parametrize("delimiter, list, result", [
        ("", [], ""),
        ("_", [""], ""),
        ("", ["", ""], ""),
        ("", ["1", "_", "ё"], "1_ё"),
        ("_", ["", "", ""], "__"),
    ])
    def test_join(self, delimiter, list, result):
        assert delimiter.join(list) == result

    @pytest.mark.parametrize("string, start, start_flag", [
        ("", "", True),
        ("ёёё", "", True),
        ("ё", "ё", True),
        ("ё___", "ё", True),
        ("___ё", "ё", False),
    ])
    def test_startswith(self, string, start, start_flag):
        assert string.startswith(start) == start_flag

    @pytest.mark.parametrize("string, length", [
        ("", 0),
        ("123", 3),
        ("ёёёёё", 5),
        ("abcde", 5),
    ])
    def test_len(self, string, length):
        assert len(string) == length

    @pytest.mark.parametrize("string, replace_from, replace_to, count, result", [
        ("", "", "", 0, ""),
        ("", "", "", 3, ""),
        ("", "", "_", 1, ""),
        ("", "", "_", -1, "_"),
        ("123321", "2", "_", 1, "1_3321"),
        ("123321", "2", "_", 2, "1_33_1"),
        ("123321", "2", "_", -1, "1_33_1"),
    ])
    def test_replace(self, string, replace_from, replace_to, count, result):
        assert string.replace(replace_from, replace_to, count) == result
