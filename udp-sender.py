import socket
import time

TOTAL = 2000
BURST = 20  # packets sent back-to-back; higher = more loss, 1 = almost none
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for seq in range(TOTAL):
    payload = f"{seq:08d}".encode() + b"x" * 1000  # 8-digit sequence number + filler
    sock.sendto(payload, ("127.0.0.1", 5005))
    if seq % BURST == BURST - 1:
        time.sleep(0.02)  # pause between bursts

print(f"Sent {TOTAL} packets")