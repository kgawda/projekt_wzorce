from dataclasses import dataclass
import datetime
from enum import Enum


class GreetingType(Enum):
    Official = "official"
    Unofficial = "unofficial"


def greet_official(name:str):
    print(f"Welcome dear {name}")

def greet_non_official(name:str):
    print(f"Hi {name}!")

GREETERS = {
    GreetingType.Official: greet_official,
    GreetingType.Unofficial: greet_non_official,
}
def select_greeter(greeting_type: GreetingType):
    # if greeting_type not in GREETERS:
    #     raise Exception(...)
    # return greeter

    # try:
    #     return GREETERS[greeting_type]
    # except KeyError as e:
    #     raise Exception("...") from e
    
    greeter = GREETERS.get(greeting_type)
    if greeter is None:
        raise Exception(...)
    return greeter


def greet(name:str, greeting_type:GreetingType):
    greeter = select_greeter(greeting_type)
    greeter(name)


@dataclass(frozen=True)
class TimeDuration:
    amount: int
    unit: str

def get_args():
    # return 5, "day"
    return TimeDuration(4, "day")


class Schedule:
    def __init__(self, interval: TimeDuration) -> None:
        timedelta_kwargs = {}
        timedelta_kwargs[interval.unit + "s"] = interval.amount
        self.interval = datetime.timedelta(**timedelta_kwargs)

class Schedule2:
    def __init__(self, interval: datetime.timedelta) -> None:
        self.interval = interval

def get_schedule2(interval: TimeDuration):
    timedelta_kwargs = {}
    timedelta_kwargs[interval.unit + "s"] = interval.amount
    interval_normalized = datetime.timedelta(**timedelta_kwargs)
    return Schedule2(interval_normalized)

if __name__ == "__main__":
    greet("Konrad", GreetingType.Official)
    greet("Konrad", GreetingType.Unofficial)

    schedule = Schedule(get_args())
    print(schedule.interval)