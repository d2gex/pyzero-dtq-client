from os.path import join
from pathlib import Path

path = Path(__file__).resolve()
ROOT = path.parents[1]
TEST = join(ROOT, 'tests')

TCP_PRODUCER_ADDRESS = "127.0.0.1"
TCP_SUBSCRIBER_ADDRESS = "127.0.0.1"

TCP_PORT_5556 = "5556"
TCP_PORT_5557 = "5557"
TCP_PROTOCOL = "tcp://"

TCP_SINK_URL_SOCKET = TCP_PROTOCOL + TCP_PRODUCER_ADDRESS + ":" + TCP_PORT_5556
TCP_PRODUCER_URL_SOCKET = TCP_SINK_URL_SOCKET
TCP_PUBLISHER_URL_SOCKET = TCP_PROTOCOL + TCP_SUBSCRIBER_ADDRESS + ":" + TCP_PORT_5557
TCP_SUBSCRIBER_URL_SOCKET = TCP_PUBLISHER_URL_SOCKET
