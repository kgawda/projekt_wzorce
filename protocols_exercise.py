import sys
from typing import Protocol

# TODO: SupportsWrite

def write_log(msg: str, target: SupportsWrite):
    target.write(msg)


if __name__ == "__main__":
    write_log("ok", sys.stdout)
    with open("temp.txt", "w") as f:
        write_log("ok", f)
