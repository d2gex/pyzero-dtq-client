from tests.stubs import AppStub


def test_app_stub_only_run_once():
    '''Ensure the AppStub used for the functional test runs only once
    '''

    app = AppStub()
    assert not app.done()

    task = [x for x in range(10)]
    assert app.get_task() == task
    assert not app.get_task()
    assert not app.done()

    app.add_result('something')
    assert  app.done()
