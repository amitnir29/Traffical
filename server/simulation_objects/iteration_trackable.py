from abc import ABCMeta
from functools import partialmethod


def activate(self, *args, activation_method, **kwargs):
    activation_method(self, *args, **kwargs)
    self._iteration += 1


@property
def iteration(self):
    return self._iteration


def iteration_trackable(cls):
    assert hasattr(cls, "activate")

    cls._iteration = 0
    cls.iteration = iteration

    cls.activate = partialmethod(activate, activation_method=cls.activate)

    return cls


class IterationTrackable(ABCMeta):
    def __new__(*args, **kwargs):
        cls = type.__new__(*args, **kwargs)
        return iteration_trackable(cls)
