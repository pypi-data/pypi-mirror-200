def forward_to(host, guest_name: str):
    def ga(self, attr):
        guest_obj = getattr(self, guest_name)
        return getattr(guest_obj, attr)

    def sa(self, key, value):
        if key == guest_name:
            super(host, self).__setattr__(key, value)
        else:
            guest_obj = getattr(self, guest_name)
            setattr(guest_obj, key, value)

    host.__getattr__ = ga
    host.__setattr__ = sa

    return host


### tests

class Guest:
    def __init__(self, string: str):
        self.string = string

    def foo(self):
        return self.string


class Host1:
    def __init__(self, guest):
        self.guest = guest
        self.prop1 = "prop1-val"

    def bar(self):
        return self.prop1


def test_proxy():
    class Host2:
        def __init__(self, guest):
            self._guest = guest

    forward_to(Host1, 'guest')
    target1 = Host1(Guest("foo"))
    assert target1.foo() == "foo"

    forward_to(Host2, '_guest')
    target2 = Host2(Guest("bar"))
    assert target2.foo() == "bar"


def test_non_existant():
    forward_to(Host1, 'guest')
    target1 = Host1(Guest("foo"))
    try:
        target1.does_not_exist()
        exception = None
    except Exception as ex:
        exception = ex

    assert exception is not None


def test_shouldNotForward_existingHostMethods():
    forward_to(Host1, 'guest')
    target1 = Host1(Guest("foo"))
    assert "prop1-val" == target1.bar()
    assert "prop1-val" == target1.prop1


def test_shouldForwardSet():
    forward_to(Host1, 'guest')
    guest = Guest("foo")
    target1 = Host1(guest)

    target1.guestprop1 = "hello"
    assert "hello" == guest.guestprop1


def test_HostSetter():
    class HostLoc:
        def __init__(self, guest):
            self.guest = guest
            self.prop1 = "prop1-val"

        def reset(self):
            self.guest.string = self.prop1

    forward_to(HostLoc, 'guest')

    guest = Guest("init")
    target = HostLoc(guest)
    target.prop1 = "changed1"
    target.reset()
    assert "changed1" == target.string
    # assert not hasattr(guest, 'prop1')
