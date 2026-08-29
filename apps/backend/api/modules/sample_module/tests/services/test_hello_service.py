from modules.sample_module.services.hello_service import HelloService


def test_say_hello() -> None:
    assert HelloService().say_hello() == "Hello, world"
