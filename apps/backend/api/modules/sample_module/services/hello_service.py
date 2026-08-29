"""Hello greeting use case — business logic lives in the service class."""


class HelloService:

    @staticmethod
    def say_hello() -> str:
        return "Hello, world"
