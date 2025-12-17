from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import shutil
from pathlib import Path

class NetworkError(Exception):
    pass

def download_gitignore(language: str) -> str:
    # simulated request.get(...)
    raise NetworkError("Connection timeout while fetching .gitignore")


@dataclass
class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

@dataclass
class CreateDirCommand(Command, ABC):
    path: str
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

@dataclass
class CreateFileCommand(Command, ABC):
    path: str
    content: str
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...


@dataclass
class CreateDirFilesystemCommand(CreateDirCommand):
    def execute(self): ...
    def undo(self): ...

@dataclass
class CreateFileFilesystemCommand(CreateFileCommand):
    def execute(self): ...
    def undo(self): ...

class AbstractTransaction(ABC):
    @abstractmethod
    def add_command(self, command: Command): ...
    @abstractmethod
    def commit(self): ...

class Transaction(AbstractTransaction):
    def __init__(self) -> None:
        self.commands: list[Command] = []

    def add_command(self, command: Command):
        self.commands.append(command)
    
    def commit(self):
        try:
            done_commands = []
            for command in self.commands:
                command.execute()
                done_commands.append(command)
        except:
            for command in done_commands[::-1]:
                command.undo()
            raise


def create_project_structure(project_name: str, transaction:AbstractTransaction, create_dir_class: type[CreateDirCommand], create_file_class: type[CreateFileCommand]):
    # TODO: jak elegancko wstrzyknąć zależność od create_dir_class i create_file_class

    root = Path(project_name)
    
    print(f"Creating project '{project_name}'...")

    transaction.add_command(create_dir_class(str(root)))

    src = root / "src"
    transaction.add_command(create_dir_class(str(src)))

    main_file = src / "main.py"
    main_file_content = "print('Hello World')"
    transaction.add_command(create_file_class(str(main_file), main_file_content))

    content = download_gitignore("python")
    transaction.add_command(create_file_class(str(root / ".gitignore"), content))

    transaction.commit()


if __name__ == "__main__":
    try:
        transaction = Transaction()
        create_project_structure("my_new_app", transaction, CreateDirFilesystemCommand, CreateFileFilesystemCommand)
    except Exception:
        print("\nFailed. Check your directory - it's probably messy now.")