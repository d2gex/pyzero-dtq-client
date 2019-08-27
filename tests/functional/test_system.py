import time
import multiprocessing

from pubsub_zmq.publisher import Publisher
from producer_sink.sink import Sink
from pyzero_dtq_client.client import Client
from tests import utils as test_utils, stubs


class TestSystem:

    topic = 'A'

    def start_server(self):
        '''It emulates the server at the other side by listening to a socket for incoming tasks and sending back the
        results of applying such task. It will wait 1 seconds to ensure the client had time to send the task over and
        then sends right away the results.
        '''
        sink = Sink(identity='TestSink', url=test_utils.TCP_SINK_URL_SOCKET)
        publisher = Publisher(identity='TestPublsher', url=test_utils.TCP_PUBLISHER_URL_SOCKET)

        time.sleep(2)
        info = sink.run()
        publisher.run(topic=self.topic, data=sum(info))
        time.sleep(0.1)

        publisher.clean()
        sink.clean()

    def test_functionality(self):
        '''Initiates a child server process while the client is run as the main parent one. It will assert that the
        results sent from the server are the ones expected.
        '''
        server_process = multiprocessing.Process(target=self.start_server)
        server_process.start()

        client = Client(producer_url=test_utils.TCP_PRODUCER_URL_SOCKET,
                        subscriber_url=test_utils.TCP_SUBSCRIBER_URL_SOCKET,
                        topics=self.topic)
        client.init_sockets()
        client.app = stubs.AppStub()
        # Let's give ZeroMQ time enough to set up the queues of the client
        time.sleep(0.5)
        # Run approximtely for 10000 * 10 ms ~ 10 seconds. It should stop way before however this is a safety net
        # to avoid the tests lingering forever if something goes wrong
        client.run(loops=10000)
        server_process.join()
        app = stubs.AppStub()
        results = sum(app.get_task())
        assert results == client.results.pop()[-1]
