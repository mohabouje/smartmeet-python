import numpy as np
from smartmeet.core.filter import Filter
from smartmeet.utils.converter import Converter
from webrtcvad import Vad

class VAD(Filter):

    def __init__(self, rate: int, mode: int = None, name: str = ""):
        """
        Creates a VAD detector with the given configuration
        Args:
            rate (int): The audio sample rate, in Hz.
            mode (int): Operational mode, must be [0, 3]
            name (str): Name of the element
        """
        super().__init__(name=name)
        self.__rate = rate
        self.__mode = mode
        self.__vad = Vad(mode=mode)

    @property
    def mode(self) -> int:
        """ Returns an integer representing the operational mode"""
        return self.__mode

    @property
    def sample_rate(self) -> int:
        """ Returns the sampling rate in Hz."""
        return self.__rate

    @mode.setter
    def mod(self, mode: int):
        """
        Set the operational mode of the VAD
        Args:
            mode (int): Operational moder, must be [0, 3]
        """
        self.__mode = mode
        self.__vad.set_mode(mode)

    def process(self, data, extra) -> tuple:
        """
        Checks if the given data contains human speech.
        Args:
            data: An array containing the data
            extra: Dictionary storing any extra information previously computed.

        Returns:
            A tuple with the original data an a boolean representing if the audio data contains speech
            in the dictionary with the key "vad"
        """
        mono = np.mean(a=data, axis=0, dtype=np.float32)
        mono = Converter.fromFloat16ToS16(mono)
        extra["vad"] = self.__vad.is_speech(buf=mono, sample_rate=self.sample_rate, length=data.size())
        return data, extra