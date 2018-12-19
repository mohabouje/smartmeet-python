from smartmeet.core.filter import Filter
from smartmeet.utils.converter import Converter
from webrtc_audio_processing import AudioProcessingModule as AP

class NoiseSuppressor(Filter):

    def __init__(self, rate: int, channels: int, name: str = ""):
        """
        Creates a noise suppression element with the given configuration
        Args:
            rate (int): The audio sample rate, in Hz.
            channels (int): Number of channels
            name (str): Name of the element
        """
        super().__init__(name=name)
        self.__channels = channels
        self.__rate = rate
        self.__frames_per_channel = int(rate * 0.01)
        self.__ap = AP(enable_ns=True)
        self.__ap.set_stream_format(rate, channels)

    @property
    def sample_rate(self) -> int:
        """ Returns the sampling rate in Hz """
        return self.__rate

    @property
    def channels(self) -> int:
        """ Returns the number of channels """
        return self.__channels

    def process(self, data, extra) -> tuple:
        if data.shape() != [self.channels, self.__frames_per_channel]:
            raise ValueError("Invalid shape. Expected (%d, %d)" % (self.channels, self.__frames_per_channel))

        data = Converter.fromFloat16ToS16(data)
        data = self.__ap.process_stream(data)
        data = Converter.fromS16ToFloat16(data)
        return data, extra