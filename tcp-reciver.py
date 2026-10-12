import socket
import time

PACKET_SIZE = 1008  # 8-digit sequence number + 1000 bytes of filler (same as the UDP test)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)  # same tiny buffer as the UDP test
server.bind(("127.0.0.1", 5006))
server.listen(1)
print("Waiting for sender... (run tcp_sender.py now)")

conn, _ = server.accept()
received = []

def slow_down(seconds):
    # busy-wait: time.sleep() is too imprecise on Windows
    end = time.perf_counter() + seconds
    while time.perf_counter() < end:
        pass

def read_exact(sock, n):
    # TCP is a byte stream, so keep reading until we have a full packet
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:  # sender closed the connection
            return None
        buf += chunk
    return buf

start = time.perf_counter()
with conn:
    while True:
        packet = read_exact(conn, PACKET_SIZE)
        if packet is None:
            break
        received.append(int(packet[:8]))
        slow_down(0.0003)  # same slow receiver as the UDP test
elapsed = time.perf_counter() - start
server.close()

if received:
    got = set(received)
    expected = max(received) + 1
    print(f"\nReceived {len(got)} of {expected}, lost {expected - len(got)}")
    print(f"Out of order: {'yes' if received != sorted(received) else 'no'}")
    print(f"Duplicates:   {len(received) - len(got)}")
    print(f"Time taken:   {elapsed:.2f}s")
    print("\n# = arrived, . = lost\n")
    for start_seq in range(0, min(expected, 600), 100):
        print("".join("#" if s in got else "." for s in range(start_seq, min(start_seq + 100, expected))))
else:
    print("Nothing received.")