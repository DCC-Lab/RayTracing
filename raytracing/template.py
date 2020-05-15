
class DocStringTemplate:
    """ The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.
    """
    def __init__(self):
        pass

    def add(self, a: float, b: float) -> float:
        """This is an example of a module level function.

        Function parameters should be documented in the ``Args`` section. The name
        of each parameter is required. The type and description of each parameter
        is optional, but should be included if not obvious.

        If ``*args`` or ``**kwargs`` are accepted,
        they should be listed as ``*args`` and ``**kwargs``.

        The format for a parameter is::

            name (type): description
                The description may span multiple lines. Following
                lines should be indented. The "(type)" is optional.

                Multiple paragraphs are supported in parameter
                descriptions.

        Args:
            param1 (int): The first parameter.
            param2 (:obj:`str`, optional): The second parameter. Defaults to None.
                Second line of description should be indented.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: True if successful, False otherwise.

            The return type is optional and may be specified at the beginning of
            the ``Returns`` section followed by a colon.

            The ``Returns`` section may span multiple lines and paragraphs.
            Following lines should be indented to match the first line.

            The ``Returns`` section supports any reStructuredText formatting,
            including literal blocks::

                {
                    'param1': param1,
                    'param2': param2
                }

        Raises:
            AttributeError: The ``Raises`` section is a list of all exceptions
                that are relevant to the interface.
            ValueError: If `param2` is equal to `param1`.

        Examples:
            Examples should be written in doctest format, and should illustrate how
            to use the function.

            >>> add(4, 28)
            32

        """

        return a + b
