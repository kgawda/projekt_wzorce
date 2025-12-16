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


if __name__ == "__main__":
    greet("Konrad", GreetingType.Official)
    greet("Konrad", GreetingType.Unofficial)