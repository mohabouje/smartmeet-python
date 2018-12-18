from queue import Queue
from pyaudio import PyAudio, paFloat32, paContinue
from smartmeet.core.element import Element


class Recorder(Element):
    """
    This class is an interface to pyAudio that performs the retrieval of recorded audio buffers
    from an input device.
    """
    def __init__(self, rate: int = 16000, frames_per_buffer: int = None,
                 channels: int = 1, device_name: int = None, name: str = ""):
        """ Creates an instance of a Recorder source with the given configuration

        :param rate: Sampling rate in Hz
        :param channels: Number of channels
        :param device_name: Input device name
        :param frames_per_buffer: Number of frames per buffer.
        """
        super().__init__(name)
        self.__queue = Queue()
        self.__rate = rate
        self.__frames_per_buffer = frames_per_buffer if frames_per_buffer else rate / 100
        self.__channels = channels
        self.__instance = PyAudio()
        self.__device_index = self.__instance.get_default_input_device_info()['index']

        if device_name:
            for i in range(self.__instance.get_device_count()):
                dev = self.__instance.get_device_info_by_index(i)
                name = dev['name'].encode('utf-8')
                if name.find(device_name) >= 0:
                    self.__device_index = i

        if self.__device_index is None:
            raise ValueError('Can not find the input device {}'.format(device_name))

        self.__stream = self.__instance.open(
            start=False,
            format=paFloat32,
            input_device_index=self.__device_index,
            channels=self.__channels,
            rate=int(self.__rate),
            frames_per_buffer=int(self.__frames_per_buffer),
            stream_callback=self.__audio_callback(),
            input=True
        )

    def __audio_callback(self, in_data, frame_count, time_info, status):
        self.__queue.put(in_data)
        return None, paContinue

    @property
    def sample_rate(self) -> int:
        """ Return the sampling rate in Hz. """
        return self.__rate

    @property
    def channels(self):
        """ Return the number of channels. """
        return self.__channels

    @property
    def device_name(self):
        """ Return the device name. """
        return self.__instance.get_device_info_by_index(self.__device_index)["name"]

    @property
    def frames_per_buffer(self):
        """ Returns the number of frames per channel"""
        return self.__frames_per_buffer

    def process(self, data=None, extra=None):
        """ Returns the oldest recorded buffer
        :param data: An array containing the data
        :param extra: Dictionary storing any extra information previously computed.
        :return: Array containing the samples read from a file
        """
        if self.__queue.empty():
            return None, extra

        return self.__queue.get(), extra

    def start(self):
        """ Starts the audio streaming """
        self.__stream.start_stream()

    def stop(self):
        """ Stops the audio streaming """
        self.__stream.stop_stream()
