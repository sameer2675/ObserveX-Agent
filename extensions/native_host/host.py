import sys
import json
import struct
import socket
AGENT_HOST = "127.0.0.1"
AGENT_PORT = 5055

def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    length = struct.unpack(
        "I",
        raw_length
    )[0]
    data = sys.stdin.buffer.read(length)

    return json.loads(
        data.decode("utf-8")
    )

def send_message(message):
    encoded = json.dumps(message).encode("utf-8")
    sys.stdout.buffer.write(
        struct.pack("I", len(encoded))
    )

    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

def send_to_agent(data):
    try:
        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        client.connect(
            (
                AGENT_HOST,
                AGENT_PORT
            )
        )
        print("Sending to Agent:", data, file=sys.stderr)
        client.send(
            json.dumps(data).encode()
        )
        client.close()
        return True
    except Exception as e:
        print(
            "Agent connection error:",
            e,
            file=sys.stderr
        )

        return False
while True:
    try:
        message = read_message()
        if message is None:
            break
        print(
            "Received from Chrome:",
            message,
            file=sys.stderr
        )

        success = send_to_agent(message)
        if success:
            send_message(
                {
                    "status": "forwarded"
                }
            )
        else:
            send_message(
                {
                    "status": "agent_offline"
                }
            )
    except Exception as e:
        print(
            "HOST ERROR:",
            e,
            file=sys.stderr
        )
        send_message(
            {
                "status": "error",
                "message": str(e)
            }
        )