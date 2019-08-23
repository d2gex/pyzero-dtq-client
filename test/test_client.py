import pytest

from pyzero_dtq_client import client
from pyzero_dtq_client.application import Application
from unittest.mock import MagicMock
from test import utils as test_utils


@pytest.fixture
def dummy_client():
    return client.Client(
        producer_url=test_utils.TCP_PRODUCER_URL_SOCKET,
        subscriber_url=test_utils.TCP_SUBSCRIBER_URL_SOCKET,
        topics='A'
    )


def test_app_setter_property(dummy_client):
    '''Ensure than when an app is provided via @app property, this is a subclass of Application
    '''

    with pytest.raises(ValueError):
        dummy_client.app = MagicMock()

    class AppSubclass(Application):

        def run(self, task):
            pass
    dummy_client.app = AppSubclass


def test_init_clean(dummy_client):

    assert not dummy_client.producer
    assert not dummy_client.subscriber
    dummy_client.init_sockets()
    assert not dummy_client.producer.socket.closed
    assert not dummy_client.subscriber.socket.closed
    dummy_client.clean()
    assert dummy_client.producer.socket.closed
    assert dummy_client.subscriber.socket.closed
