from __future__ import annotations


class AnnotationLabel(object):

    def __init__(self, name: str = None, color: str = None):
        self._name = name
        self._color = color

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color) -> None:
        self._color = color

    def as_dict(self) -> dict:
        """
        Creates a dictionary representation of this object.

        Returns
        -------
        d:
            A dictionary with all of the properties as keys and the property values as values.
        """
        d = {}
        for k, v in vars(self).items():
            d[k[1:]] = v
        return d

    @staticmethod
    def from_dict(object_dict) -> AnnotationLabel:
        """
        Creates an AnnotationLabel object from the dictionary representation.

        Parameters
        ----------
        object_dict:
            A dictionary with all of the properties as keys and the property values as values.

        Returns
        -------
        annotation_label:
            An AnnotationLabel object.
        """
        annotation_label = AnnotationLabel(name=object_dict.get('name'), color=object_dict.get('color'))
        return annotation_label
