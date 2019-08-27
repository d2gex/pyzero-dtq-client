import pytest

from pyzero_dtq_client.application import Application


def test_application_class_to_be_extended():

    class A(Application):
        pass
    with pytest.raises(TypeError):
        A()

    class B(Application):
        def get_task(self):
            pass
    with pytest.raises(TypeError):
        B()

    class C(B):
        def add_result(self, result):
            pass
    with pytest.raises(TypeError):
        C()

    class D(C):
        def get_results(self):
            pass

    with pytest.raises(TypeError):
        D()

    class E(D):
        def done(self):
            pass

    E()