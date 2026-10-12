import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)  # small buffer so it overflows
sock.bind(("127.0.0.1", 5005))
sock.settimeout(3)  # stop after 3 seconds of silence

received = set()
print("Waiting for packets... (run sender.py now)")

def slow_down(seconds):
    # busy-wait: time.sleep() is too imprecise on Windows
    end = time.perf_counter() + seconds
    while time.perf_counter() < end:
        pass

try:
    while True:
        data, _ = sock.recvfrom(2048)
        received.add(int(data[:8]))
        slow_down(0.0003)  # simulate a slightly slow receiver
except socket.timeout:
    pass

if received:
    expected = max(received) + 1
    print(f"\nReceived {len(received)} of {expected}, lost {expected - len(received)}")
    print("\n# = arrived, . = lost\n")
    for start in range(0, min(expected, 600), 100):
        print("".join("#" if s in received else "." for s in range(start, min(start + 100, expected))))
else:
    print("Nothing received.")