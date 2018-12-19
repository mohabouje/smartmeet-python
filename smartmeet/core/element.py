from abc import ABC


class Element(ABC):
    """For the application programmer, elements are best visualized as black
    boxes. On the one end, you might put something in, the element does
    something with it and something else comes out at the other side.

    There are three different types of elements:

    * Source Elements generate data for use by a pipeline. Source elements do
      not accept data, they only generate data.

    * Filter Elements have both input and outputs pads. They operate on data
      that they receive on their input (sink) pads, and will provide data on
      their output (io) pads.

    * Sink Elements are end points in a media pipeline. They accept data but do
      not produce anything.

    By linking a io element with zero or more filter-like elements and
    finally a sink element, you set up a media pipeline. Data will flow through
    the elements. This is the basic concept of media handling.
    """

    def __init__(self, name: str = ""):
        """Creates an Element with the given alias

        Args:
            name (str): Element's name also known as alias
        """
        self.__name = name

    @property
    def name(self) -> str:
        """Returns the name (also known as alias) of the Element"""
        return self.__name
