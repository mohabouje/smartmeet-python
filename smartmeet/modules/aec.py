import numpy as np
from speexdsp import EchoCanceller
from smartmeet.core.filter import Filter
from smartmeet.utils.converter import Converter


class AEC(Filter):

    def __init__(self, channels: int, rate: int, frames_per_channel: int, filter_length: int, name: str = ""):
        super().__init__(name=name)
        self.__channels = channels
        self.__rate = rate
        self.__frames_per_channel = frames_per_channel
        self.__filter_length = filter_length
        self.__aec = [EchoCanceller.create(frame_size=frames_per_channel,
                                           filter_length=filter_length,
                                           sample_rate=rate)] * channels

    @property
    def sample_rate(self) -> int:
        """ Returns the sampling rate in Hz """
        return self.__rate

    @property
    def channels(self) -> int:
        """ Returns the number of channels """
        return self.__channels


    def process(self, data, playback):
        """
        Removes the influence of the playback data from the recorded
        Args:
            data: An array containing the data
            extra: Dictionary storing any extra information previously computed.

        Returns:
            A tuple with the filtered data
        """

        if data.shape() != [self.channels, self.__frames_per_channel]:
            raise ValueError("Invalid shape. Expected (%d, %d)" % (self.channels, self.__frames_per_channel))


        mono_playback = np.mean(a=playback, axis=0, dtype=np.float32)
        mono_playback = Converter.fromFloat16ToS16(mono_playback)

        for i in range(self.__channels):
            temp = Converter.fromFloat16ToS16(data[i][:])
            temp = Converter.interleave(temp)
            temp = self.__aec[i].process_stream(temp, mono_playback)
            floating = Converter.deinterleave(temp, channels=1, frames_per_buffer=self.__frames_per_channel)
            floating = Converter.fromS16ToFloat16(floating)
            data[i][:] = floating
        return data