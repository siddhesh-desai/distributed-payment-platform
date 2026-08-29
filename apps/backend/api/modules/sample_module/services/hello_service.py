"""Hello greeting use case — business logic lives in the service class."""


class HelloService:
    """Greeting use case; construct and inject (same-module DI)."""

    def say_hello(self) -> str:
        return "Hello, world"
