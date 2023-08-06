from typing import Optional, Dict, List

from .finder import _find_all, _find


class HTMLElement():
    def __init__(self,
                 tagname: str,
                 closed: bool = False,
                 attrs=None,
                 text: str = "",
                 _all_text=[],
                 descendants=[],
                 _children=[],
                 parent=None,
                 previous_sibling=None,
                 next_sibling=None
                 ):
        self.tagname = tagname
        self.attrs = attrs
        self.text = text
        self._all_text = _all_text
        self.closed = closed
        self.descendants = descendants
        self._children = _children
        self.parent = parent
        self.previous_sibling = previous_sibling
        self.next_sibling = next_sibling

    def __repr__(self) -> str:
        return f"{self.tagname.upper()} attrs={self.attrs} text={self.text}"

    def find_all(self, tag: str, attrs: Optional[Dict[str, str | None]] = None, exclude_attrs: Optional[Dict[str, List[str | None]]] = None):
        """Return all matching elements"""
        return _find_all(self.descendants, tag, attrs, exclude_attrs)

    def find(self, tag: str, attrs: Optional[Dict[str, str | None]] = None, exclude_attrs: Optional[Dict[str, List[str | None]]] = None):
        """Return first matching element"""
        return _find(self.descendants, tag, attrs, exclude_attrs)

    @property
    def children(self):
        """Return elements one level down"""
        self._children.reverse()
        return self._children

    @property
    def all_text(self) -> str:
        """Return all text within element"""
        res = ""
        for text_or_obj in self._all_text:
            if type(text_or_obj) == str:
                res += text_or_obj
                continue
            res += text_or_obj.all_text
        return res
