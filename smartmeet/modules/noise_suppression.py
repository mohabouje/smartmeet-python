from numpy import ndarray
from smartmeet.utils.converter import Converter
from profilehooks import profile
from webrtc_audio_processing import AudioProcessingModule as AP

class NoiseSuppressor:
    """
    This NoiseSuppressor class implements a basic noise suppression algorithm that tries to remove the noising background
    from an input signal.

    Notes:
        This algorithm implements a Noise Suppression technique, not Active Noise Cancellation.

    """
    def __init__(self, rate: int, channels: int, level: int = 0):
        """Creates a noise suppression element with the given configuration

        Args:
            rate (int): The audio sample rate, in Hz.
            channels (int): Number of channels
            level (int):  Level of aggressiveness of the noise suppression algorithm.
        """
        self.__channels = channels
        self.__rate = rate
        self.__frames_per_channel = int(rate * 0.01)
        self.__ap = AP(enable_ns=True)
        self.__ap.set_stream_format(rate, channels)

    @property
    def sample_rate(self) -> int:
        """Returns the sampling rate in Hz"""
        return self.__rate

    @property
    def channels(self) -> int:
        """Returns the number of channels"""
        return self.__channels

    @property
    def level(self) -> int:
        """Level of aggressiveness of the noise suppression algorithm"""
        return self.__ap.ns_level()

    @level.setter
    def level(self, level: int):
        """This changes the aggressiveness of the noise suppression method.

        Different levels:
        -0 : Mild (6 dB)
        *1 : Medium (10 dB)
        -2 : Aggressive (15 dB)

        Args:
            level (int): Level of aggressiveness of the noise suppression
                algorithm.
        """
        self.__ap.set_ns_level(level)

    @profile
    def process(self, data : ndarray) -> ndarray:
        """Applies a de-noising filter to the input data

        Args:
            data (ndarray): An array containing the data

        Returns:
            An array containing the clean data.

        Note:
            This class operates only with buffers of 10 milliseconds. For
            instance, if the class is using 2 channels and a sampling rate of
            8KHz, the processing function is expecting an numpy.ndarray of shape
            [0.01 * SampleRate, Channels] = [80, 2]
        """
        if data.shape != [self.__frames_per_channel, self.channels]:
            raise ValueError("Invalid shape. Expected (%d, %d)" % (self.channels, self.__frames_per_channel))

        fixed = Converter.fromFloat16ToS16(data)
        fixed = Converter.interleave(fixed)
        fixed = self.__ap.process_stream(fixed)
        floating = Converter.fromS16ToFloat16(fixed)
        floating = Converter.deinterleave(data=floating, channels=self.channels, frames_per_buffer=self.__frames_per_channel)
        return floating