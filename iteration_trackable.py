from functools import partialmethod


def activate(self, *args, activation_method, **kwargs):
    self._iteration += 1
    activation_method(self, *args, **kwargs)


@property
def iteration(self):
    return self._iteration


def iteration_trackable(cls):
    assert hasattr(cls, "activate") and not hasattr(cls, "_activate")
    assert not hasattr(cls, "iteration") and not hasattr(cls, "_iteration")

    cls._iteration = 0
    cls.iteration = iteration

    cls.activate = partialmethod(activate, activation_method=cls.activate)

    return cls
