import pytest

from idact.detail.deployment.cancel_on_failure import cancel_on_failure


class Cancellable:
    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True


def test_should_not_cancel_on_exit():
    cancellable = Cancellable()
    with cancel_on_failure(cancellable):
        pass
    assert cancellable.cancelled is False


def test_should_cancel_on_failure():
    cancellable = Cancellable()
    with pytest.raises(ValueError):
        with cancel_on_failure(cancellable):
            raise ValueError()
    assert cancellable.cancelled
