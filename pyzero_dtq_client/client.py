import uuid

from pyzero_dtq_client.iprocess import IProcess
from pyzero_dtq_client.application import Application
from pubsub_zmq.subscriber import Subscriber
from producer_sink.producer import Producer


class Client(IProcess):

    def __init__(self, producer_url, subscriber_url, topics):
        super().__init__()
        self.producer_url = producer_url
        self.subscriber_url = subscriber_url
        self.topics = topics
        self.producer_id = f"{str(uuid.uuid4()).replace('_', '')}_producer"
        self.subscriber_id = f"{str(uuid.uuid4()).replace('_', '')}_subscriber"
        self.producer = None
        self.subscriber = None
        self._app = None

    @property
    def results(self):
        return self._app.get_results()

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, application):
        if not issubclass(application, Application):
            raise ValueError(f"'application' argument should be a subclass of {Application}")
        self._app = application

    def init_sockets(self):
        self.producer = Producer(identity=self.producer_id, url=self.producer_url)
        self.subscriber = Subscriber(topics=self.topics, identity=self.subscriber_id, url=self.subscriber_url)

    def clean(self):
        if self.producer:
            self.producer.clean()
        if self.subscriber:
            self.subscriber.clean()

    def run(self, loops=True):
        stop = False

        try:
            while not stop and loops:
                if self.app.done():
                    stop = True
                else:
                    # Send tasks if any
                    task = self.app.get_task()
                    if task:
                        self.producer.run(data=task)
                    # Get results if any
                    result = self.subscriber.run()
                    if result:
                        self.app.add_result(result)
                if not stop and not isinstance(loops, bool):
                    loops -= 1
        except KeyboardInterrupt:
            pass
        finally:
            self.clean()
