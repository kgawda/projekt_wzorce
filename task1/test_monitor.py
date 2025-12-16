
from sys_monitor2 import SystemMonitor, Publisher, SystemSource, StrFormatter
from sys_monitor2 import SystemUsage

class StaticSystemSource(SystemSource):
    def __init__(self, cpu, ram) -> None:
        self.cpu = cpu
        self.ram = ram

    def get_metrics(self) -> SystemUsage:
        return SystemUsage(cpu=self.cpu, memory=self.ram)

class SpyPublisher(Publisher):
    def __init__(self) -> None:
        self.published = []

    def publish(self, content: str) -> None:
        self.published.append(content)

def test_monitor_puslishes_basic_data():
    publisher = SpyPublisher()
    monitor = SystemMonitor(
        system_source=StaticSystemSource(cpu=1, ram=1024),
        formatter=StrFormatter(),
        publisher=publisher,
    )

    monitor.run()
    assert publisher.published == ["SystemAnalysis(cpu=1, memory=1024, warnigns=[], status='OK')"]