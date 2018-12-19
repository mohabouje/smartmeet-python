from smartmeet.core.source import Source


class Pipeline:

    def __init__(self, name: str = "default"):
        self.__name = name


    def start(self, source):
        if not issubclass(type(source), Source):
            raise TypeError("Only Source objects can start a pipeline")

        source.start()
        while not source.done():
            try:
                source.run()
            except KeyboardInterrupt:
                source.stop()
                return -1
        return 0