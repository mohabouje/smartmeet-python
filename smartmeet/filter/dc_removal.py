from scipy import signal
from profilehooks import profile
from numpy import ndarray

class DCRemoval():

    def __init__(self, rate: int, order: int = 5):
        self.__cutoff = 10.0
        self.__sos = signal.butter(N=order,
                                   Wn=2.0 * self.__cutoff / float(rate),
                                   analog=False,
                                   btype='high',
                                   output='sos')

    @property
    def cutoff(self):
        """ Returns the cut off frequency of the High-Pass filter """
        return self.__cutoff

    def freqz(self):
        """ Returns the frequency response of the filter"""
        return signal.sosfreqz(self.__sos, worN=2000)


    @profile
    def process(self, data : ndarray) -> ndarray:
        """Removes the mean value or linear trend from a N-dimensional array.

        Args:
            data (ndarray): An array containing the data

        Returns:
            An array the same size as input containing the median filtered
            result.
        """
        return signal.sosfilt(self.__sos, data)
