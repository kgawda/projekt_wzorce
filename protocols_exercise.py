import sys





def write_log(msg: str, target):
    target.write(msg)

write_log("ok", sys.stdout)
with open("temp.txt") as f:
    write_log("ok", f)
