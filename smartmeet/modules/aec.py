import numpy as np
from speexdsp import EchoCanceller
from smartmeet.utils.converter import Converter

class AEC:

    def __init__(self, channels: int, rate: int, frames_per_channel: int, filter_length: int):
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


    def process(self, data: np.ndarray, playback: np.ndarray) -> np.ndarray:
        """
        Removes the influence of the playback data from the recorded
        Args:
            data: An array containing the data
            playback: An array storing the played data

        Returns:
            An array storing the final results
        """

        if data.shape != [self.__frames_per_channel, self.channels]:
            raise ValueError("Invalid shape. Expected (%d, %d)" % (self.channels, self.__frames_per_channel))


        mono_playback = np.mean(a=playback, axis=0, dtype=np.float32)
        mono_playback = Converter.fromFloatToInt16(mono_playback)

        output = np.zeros(shape=[self.__frames_per_channel, self.channels], dtype=np.float32)
        for i in range(self.__channels):
            fixed = Converter.fromFloatToInt16(data[i][:])
            fixed = Converter.interleave(fixed)
            fixed = self.__aec[i].process_stream(fixed, mono_playback)
            fixed = Converter.deinterleave(data=fixed, channels=1, frames_per_buffer=self.__frames_per_channel, dtype=np.int16)
            output[i][:] = Converter.fromInt16ToFloat(fixed)
        return output