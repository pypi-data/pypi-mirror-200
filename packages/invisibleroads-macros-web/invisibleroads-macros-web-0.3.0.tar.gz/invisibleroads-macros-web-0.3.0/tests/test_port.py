from pytest import raises

import invisibleroads_macros_web.port as module
from invisibleroads_macros_web.port import (
    find_open_port)


def test_find_open_port(monkeypatch):
    monkeypatch.setattr(
        module, 'randint', lambda a, b: 5000)
    monkeypatch.setattr(
        module, 'is_port_in_use', lambda x: False)
    assert find_open_port() == 5000
    assert find_open_port(7000) == 7000
    monkeypatch.setattr(
        module, 'is_port_in_use', lambda x: True if x == 7000 else False)
    with raises(OSError):
        find_open_port(7000, 7000, 7000)
    assert find_open_port(7000) == 5000
