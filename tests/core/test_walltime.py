import pytest

from idact.core.walltime import Walltime


def test_walltime_values():
    """Basic walltime values."""
    walltime = Walltime(days=1, hours=2, minutes=3, seconds=4)
    assert walltime.days == 1
    assert walltime.hours == 2
    assert walltime.minutes == 3
    assert walltime.seconds == 4


def test_walltime_must_not_be_zero():
    """Zero walltime is not allowed."""
    with pytest.raises(ValueError):
        Walltime()


def test_walltime_days():
    """Values for days parameter."""
    with pytest.raises(ValueError):
        Walltime(days=-1)
    assert Walltime(days=10).days == 10


def test_walltime_hours():
    """Values for hours parameter."""
    with pytest.raises(ValueError):
        Walltime(hours=-1)
    assert Walltime(hours=10).hours == 10
    with pytest.raises(ValueError):
        Walltime(hours=24)


def test_walltime_minutes():
    """Values for minutes parameter."""
    with pytest.raises(ValueError):
        Walltime(minutes=-1)
    assert Walltime(minutes=10).minutes == 10
    with pytest.raises(ValueError):
        Walltime(minutes=60)


def test_walltime_seconds():
    """Values for seconds parameter."""
    with pytest.raises(ValueError):
        Walltime(seconds=-1)
    assert Walltime(seconds=10).seconds == 10
    with pytest.raises(ValueError):
        Walltime(seconds=60)


def test_walltime_from_string():
    """Values for walltime conversion from string."""
    walltime_1 = Walltime.from_string('1:02:03')
    assert walltime_1.days == 0
    assert walltime_1.hours == 1
    assert walltime_1.minutes == 2
    assert walltime_1.seconds == 3

    walltime_2 = Walltime.from_string('4-1:02:03')
    assert walltime_2.days == 4
    assert walltime_2.hours == 1
    assert walltime_2.minutes == 2
    assert walltime_2.seconds == 3

    walltime_3 = Walltime.from_string('4-05:02:03')
    assert walltime_3.days == 4
    assert walltime_3.hours == 5
    assert walltime_3.minutes == 2
    assert walltime_3.seconds == 3

    walltime_4 = Walltime.from_string('400-12:30:59')
    assert walltime_4.days == 400
    assert walltime_4.hours == 12
    assert walltime_4.minutes == 30
    assert walltime_4.seconds == 59

    with pytest.raises(ValueError):
        Walltime.from_string('0:00:00')
    with pytest.raises(ValueError):
        Walltime.from_string('-1:02:03')
    with pytest.raises(ValueError):
        Walltime.from_string('1:02: 03')
    with pytest.raises(ValueError):
        Walltime.from_string('02:03')
    with pytest.raises(ValueError):
        Walltime.from_string('3')
    with pytest.raises(ValueError):
        Walltime.from_string('3-4')
    with pytest.raises(ValueError):
        Walltime.from_string('3-4:05')
    with pytest.raises(ValueError):
        Walltime.from_string('1:2:3')
    with pytest.raises(ValueError):
        Walltime.from_string('abc')
