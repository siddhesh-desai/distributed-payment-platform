"""Published hello operations for HTTP and other modules."""

from modules.sample_module.services import HelloService


class HelloFacade:
    """Static facade over hello use-case services."""

    @staticmethod
    def say_hello() -> str:
        return HelloService().say_hello()
