import socket
import time

TOTAL = 2000
BURST = 20  # same burst pattern as the UDP test

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 5006))

start = time.perf_counter()
for seq in range(TOTAL):
    payload = f"{seq:08d}".encode() + b"x" * 1000
    sock.sendall(payload)  # blocks if the receiver's buffer is full
    if seq % BURST == BURST - 1:
        time.sleep(0.02)  # pause between bursts

sock.close()
print(f"Sent {TOTAL} packets in {time.perf_counter() - start:.2f}s")