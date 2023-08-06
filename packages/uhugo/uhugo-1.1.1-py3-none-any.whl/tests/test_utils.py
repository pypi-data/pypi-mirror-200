from uhugo.utils import humanise_list


def test_humanise_list():
    assert humanise_list(["a"]) == "a"
    assert humanise_list(["a", "b"]) == "a and b"
    assert humanise_list(["a", "b", "c"]) == "a, b and c"
    assert humanise_list(["a", "b", "c", "d"]) == "a, b, c and d"
