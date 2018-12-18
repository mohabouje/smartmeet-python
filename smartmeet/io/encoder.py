from soundfile import SoundFile
from smartmeet.core.element import Element


class Encoder(Element):
    """
    This class is an interface to write data into an audio file
    """
    def __init__(self, file_name: str, rate: int, channels: int, name: str = ""):
        """ Creates an instance of a Encoder source with the given configuration
        :param rate : The sample rate of the file in Hz.
        :param channels : The number of channels of the file.
        :param file_name: Input file name
        """
        super().__init__(name)
        self.__instance = SoundFile(file=file_name, mode='w', samplerate=rate, channels=channels)

    @property
    def sample_rate(self) -> int:
        """ Return the sampling rate in Hz. """
        return self.__instance.samplerate

    @property
    def channels(self):
        """ Return the number of channels. """
        return self.__instance.channels

    @property
    def file_name(self):
        """ Return the file name. """
        return self.__instance.name

    def seek(self, frames):
        """Set the write position.
        :param frames : The frame index or offset to seek.
        :returns The new absolute read/write position in frames
        """
        return self.__instance.seek(frames=frames)

    def process(self, data=None, extra=None):
        """ Writes the buffer of data into the audio file.
        :param data: An array containing the data
        :param extra: Dictionary storing any extra information previously computed.
        :return: An array the same size as the input
        """
        self.__instance.write(data=data)
        return data, extra
