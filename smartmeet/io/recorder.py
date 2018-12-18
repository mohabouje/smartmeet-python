import pyaudio
from smartmeet.core.element import Element
from queue import Queue


class Recorder(Element):
    """
    This class is an interface to pyAudio that performs the retrieval of recorded audio buffers
    from an input device.
    """
    def __init__(self,rate=16000, frames_size=None, channels=None, device_name=None, name: str = ""):
        """ Creates an instance of a Recorder source with the given configuration

        :param rate: Sampling rate in Hz
        :param channels: Number of channels
        :param device_name: Input device name
        :param frames_size: Number of frames per buffer.
        """
        super().__init__(name)
        self.__data = Queue()
        self.__rate = rate
        self.__frames_size = frames_size if frames_size else rate / 100
        self.__channels = channels if channels else 1
        self.__instance = pyaudio.PyAudio()
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
            format=pyaudio.paFloat32,
            input_device_index=self.__device_index,
            channels=self.__channels,
            rate=int(self.__rate),
            frames_per_buffer=int(self.__frames_size),
            stream_callback=self.__audio_callback(),
            input=True
        )

    def __audio_callback(self, in_data, frame_count, time_info, status):
        self.__data.put(in_data)
        return None, pyaudio.paContinue

    def process(self, data, extra=None):
        """ Returns the oldest recorded buffer
        :param data: An array containing the data to be filtered
        :param extra: Dictionary storing any extra information previously computed.
        :return: An array the same size as input containing the median filtered result.
        """
        if self.__data.empty():
            return None, extra

        return self.__data.get(), extra

    def start(self):
        """ Starts the audio streaming """
        self.__stream.start_stream()

    def stop(self):
        """ Stops the audio streaming """
        self.__stream.stop_stream()