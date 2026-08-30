"""HelloService unit tests.

- Says hello with the sample greeting message
"""

from modules.sample_module.services import HelloService


def test_say_hello() -> None:
    assert HelloService().say_hello() == "Hello, world"
