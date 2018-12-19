from soundfile import SoundFile

from smartmeet.core.source import Source


class Decoder(Source):
    """
    This class is an interface to read data from an audio file
    """

    def __init__(self, file_name: str, frames_per_buffer: int = None, name: str = ""):
        """ Creates an instance of a Decoder source with the given configuration

        :param file_name: Input file name
        :param frames_per_buffer: Number of frames per buffer.
        """
        super().__init__(name)
        self.__instance = SoundFile(file=file_name, mode='r')
        self.__frames_per_buffer = frames_per_buffer if frames_per_buffer else self.sample_rate / 100

    @property
    def sample_rate(self) -> int:
        """ Return the sampling rate in Hz. """
        return self.__instance.samplerate

    @property
    def channels(self) -> int:
        """ Return the number of channels. """
        return self.__instance.channels

    @property
    def file_name(self) -> str:
        """ Return the file name. """
        return self.__instance.name

    @property
    def frames_per_buffer(self) -> int:
        """ Returns the number of frames per channel"""
        return self.__frames_per_buffer

    def done(self) -> bool:
        """ Checks if there still data to read from the audio file """
        return self.__instance.tell() < self.__instance.frames

    def start(self):
        self.__instance.seek(0)

    def stop(self):
        self.__instance.seek(self.frames_per_buffer)

    def timestamp(self):
        return self.__instance.tell() / self.__instance.samplerate

    def seek(self, frames):
        """Set the read position.
        :param frames : The frame index or offset to seek.
        :returns The new absolute read/write position in frames
        """
        return self.__instance.seek(frames=frames)

    def process(self):
        """ Returns the buffer read from the audio file
        :param data: An array containing the data
        :param extra: Dictionary storing any extra information previously computed.
        :return: Array storing the samples read from the file
        """
        return self.__instance.read(
            frames=self.__frames_per_buffer, dtype='float32', always_2d=True)
