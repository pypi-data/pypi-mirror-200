import argparse

from fastapi_all_out.pydantic import snake_case


class CommandMC(type):
    def __new__(cls, name, bases, attrs: dict, **kwargs):
        command_name = attrs.get('name', name)
        attrs['name'] = snake_case(command_name)
        return super().__new__(cls, name, bases, attrs)


class Command(metaclass=CommandMC):
    name: str
    parser: argparse.ArgumentParser

    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def add_arguments(self):
        pass

    def run(self):
        self.add_arguments()
        self.handle(**self.parser.parse_args().__dict__)

    def handle(self, **kwargs):
        raise NotImplementedError('Хоть что-то напиши')


def list_commands():
    return tuple(map(lambda x: x.name, Command.__subclasses__()))


def run_command(name: str):
    commands = list(filter(lambda x: x.name == name, Command.__subclasses__()))
    match len(commands):
        case 1:
            commands[0]().run()
        case 0:
            print('нет такой команды :(')
        case _:
            print('Таких команд несколько')
