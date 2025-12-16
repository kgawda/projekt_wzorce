from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random
import sys
from typing import Self

@dataclass
class SystemUsage:
    cpu: int
    memory: int

@dataclass
class SystemAnalysis:
    cpu: int
    memory: int
    warnigns: list[str] = field(default_factory=list)
    status: str = "OK"

    @classmethod
    def from_system_usage(cls, system_usage: SystemUsage) -> Self:
        return cls(
            cpu = system_usage.cpu,
            memory = system_usage.memory,
        )

class SystemSource(ABC):
    @abstractmethod
    def get_metrics(self) -> SystemUsage: ...

class RandomSystemSource(SystemSource):
    def get_metrics(self) -> SystemUsage:
        return SystemUsage(
            cpu=random.randint(0, 100),
            memory=random.randint(2048, 16384)  # MB
        )

class Formatter(ABC):
    @abstractmethod
    def format(self, analysis: SystemAnalysis) -> str: ...

class StrFormatter(Formatter):
    def format(self, analysis: SystemAnalysis) -> str:
        return str(analysis)

class Publisher(ABC):
    @abstractmethod
    def publish(self, content: str) -> None: ...

class ConsolePublisher(Publisher):
    def publish(self, content: str) -> None:
        print(content)

class FilePublisher(Publisher):
    def __init__(self, file_path: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.file_path = file_path

    def publish(self, content: str) -> None:
        with open(self.file_path, "w") as f:
            f.write(content)

# TODO add warning limit arguments
def analyze_system_usage(system_usage: SystemUsage) -> SystemAnalysis:
    # TODO: add warnigns, etc.
    return SystemAnalysis.from_system_usage(system_usage)

class SystemMonitor:
    def __init__(
        self,
        system_source: SystemSource,
        publisher: Publisher,
        formatter: Formatter
    ) -> None:
        self.system_source = system_source
        self.publisher = publisher
        self.formatter = formatter

    def run(self):
        system_usage = self.system_source.get_metrics()
        system_analysis = analyze_system_usage(system_usage)
        content = self.formatter.format(system_analysis)
        self.publisher.publish(content)


def main(config):
    monitor = SystemMonitor(
        system_source = RandomSystemSource(),
        publisher = ConsolePublisher(),
        formatter = StrFormatter(),
    )
    monitor.run()


def cli_main(args):
    config = ...
    main(config)

if __name__ == "__main__":
    cli_main(sys.argv)