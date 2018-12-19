import operator
import numpy as np
from time import time
from singleton_decorator import singleton


class ProfilerReport:
    def __init__(self, label: str):
        self.__measures = np.zeros(shape=[1,], dtype=np.float64)
        self.__label = label

    @property
    def label(self):
        return self.__label

    @property
    def average(self):
        return np.mean(self.__measures)

    @property
    def worst(self):
        return np.max(self.__measures)

    @property
    def best(self):
        return np.min(self.__measures)

    @property
    def total(self):
        return np.sum(self.__measures)

    def profile(self, func, *args, **kw):
        t0 = time()
        result = func(*args, **kw)
        np.append(self.__measures, time() - t0)
        return result


@singleton
class Profiler:

    def __init__(self):
        self.__entries = dict()

    def __get_profiler(self, label: str) -> ProfilerReport:
        if label not in self.__entries:
            profiler = ProfilerReport(label=label)
            self.__entries[label] = profiler
        return self.__entries[label]

    def profile(self, label, func, *args, **kw):
        self.__get_profiler(label=label).profile(func=func, args=args, kw=kw)

    def print(self):
        for profiler in sorted(self.__entries.items(), key=operator.itemgetter(1)):
            print("Label: %s \t Total: %f \t Average: %f \t Worst: %f \t Best: %f "
                  % (profiler.label, profiler.total, profiler.average, profiler.worst, profiler.best))