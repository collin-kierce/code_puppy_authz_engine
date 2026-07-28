from detector import (
    detect_self_termination_command,
)

def test(command):
    hit = detect_self_termination_command(command)
    if hit is None:
        print("nothing here")
        return
    print(hit)

test("echo hello")
test("kill python")
test("pkill -9 code-puppy")
