import pytest

from pyzero_dtq_client import client
from pyzero_dtq_client.application import Application
from unittest.mock import MagicMock, patch
from tests import utils as test_utils


@pytest.fixture
def dummy_client():
    return client.Client(
        producer_url=test_utils.TCP_PRODUCER_URL_SOCKET,
        subscriber_url=test_utils.TCP_SUBSCRIBER_URL_SOCKET,
        topics='A'
    )


def test_app_setter_property(dummy_client):
    '''Ensure than when an app is provided via @app property, this is an instance of Application
    '''

    with pytest.raises(ValueError):
        dummy_client.app = MagicMock()

    class AppSubclass(Application):

        def get_task(self):
            pass

        def add_result(self, result):
            pass

        def get_results(self):
            pass

        def done(self):
            pass

    dummy_client.app = AppSubclass()


def test_init_clean(dummy_client):

    assert not dummy_client.producer
    assert not dummy_client.subscriber
    dummy_client.init_sockets()
    assert not dummy_client.producer.socket.closed
    assert not dummy_client.subscriber.socket.closed
    dummy_client.clean()
    assert dummy_client.producer.socket.closed
    assert dummy_client.subscriber.socket.closed


def test_task_done(dummy_client):
    '''Ensure that when ta task is done, the loops stop
    '''
    with patch.object(dummy_client, '_app') as mock_app:
        with patch.object(dummy_client, 'clean') as mock_clean:
            mock_app.done.return_value = True
            dummy_client.run(loops=1)
    mock_app.done.assert_called_once()
    mock_app.get_task.assert_not_called()
    mock_clean.assert_called_once()


def test_send_tasks_when_available_and_ignore_picking_results_when_not(dummy_client):
    '''Ensure that:

    1) Send a task via its producer socket when it is available
    2) If not results available then nothing is done
    '''
    with patch.object(dummy_client, '_app') as mock_app:
        with patch.object(dummy_client, 'clean') as mock_clean:
            with patch.object(dummy_client, 'producer') as mock_producer:
                with patch.object(dummy_client, 'subscriber') as mock_subscriber:
                    mock_app.done.return_value = False
                    mock_app.get_task.return_value = True
                    mock_subscriber.run.return_value = True
                    dummy_client.run(loops=1)

    mock_app.get_task.assert_called_once()
    mock_producer.run.assert_called_once()
    mock_subscriber.run.assert_called_once()
    mock_app.add_results.assert_not_called()
    mock_clean.assert_called_once()


def test_add_results_when_available_and_ignore_sending_tasks_when_not(dummy_client):
    '''Ensure that:

    1) Add results when available
    1) Ignore sending tasks when not available
    '''
    with patch.object(dummy_client, '_app') as mock_app:
        with patch.object(dummy_client, 'clean') as mock_clean:
            with patch.object(dummy_client, 'producer') as mock_producer:
                with patch.object(dummy_client, 'subscriber') as mock_subscriber:
                    mock_app.done.return_value = False
                    mock_app.get_task.return_value = False
                    mock_subscriber.run.return_value = False
                    dummy_client.run(loops=1)

    mock_app.get_task.assert_called_once()
    mock_producer.run.assert_not_called()
    mock_subscriber.run.assert_called_once()
    mock_app.add_results.assert_not_called()
    mock_clean.assert_called_once()
