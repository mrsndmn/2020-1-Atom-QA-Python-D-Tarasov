
import vkapi.vkapi as vkapi
import pytest

import sys

@pytest.mark.parametrize('shortname', [
    '',
    '123321', # состоит только из цифр. Это запрещено, потому что тогда в апишке вк нельзя будет различить, мы передали id или передали короткое имя
    'mrsndmn 1231', # содержит пробел
    'абвгд', # содержит кириллицу
    'mrsndmn,durov', # содержит запятую
])
def test_bad_shortnames(shortname):
    # print(vkapi.get_user_id_by_shortname)
    assert vkapi.get_user_id_by_shortname(shortname) == {}
