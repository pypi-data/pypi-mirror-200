from html.parser import HTMLParser
from typing import Optional, Dict, List

from .element import HTMLElement
from .finder import _find_all, _find


SELF_CLOSING_TAGS = ["area", "base", "br", "col", "embed", "hr", "img", "input",
                     "link", "meta", "param", "source", "track", "wbr", "command", "keygen", "menuitem"]


class Parser(HTMLParser):
    def __init__(self, html: str):
        super().__init__()
        self.html = html
        self.current_element = HTMLElement("")
        self.previous_element = HTMLElement("")
        self.elements: List[HTMLElement] = []
        self.feed(html)

    def __repr__(self) -> str:
        return f"{self.elements}"

    def handle_starttag(self, tag: str, attrs) -> None:
        new_element = HTMLElement(tag, attrs=dict(attrs))
        if self.elements:
            new_element.parent = self.current_element
            self.current_element._all_text = self.current_element._all_text + [new_element]
        if self.previous_element.closed:
            self.previous_element.next_sibling = new_element
        self.current_element = new_element
        self.elements.append(self.current_element)
        if tag in SELF_CLOSING_TAGS:
            self.current_element.closed = True

    def handle_endtag(self, tag: str) -> None:
        self.current_element.descendants = self.elements[self.elements.index(self.current_element) + 1:]
        self.current_element.closed = True
        self.previous_element = self.current_element
        ind = self.elements.index(self.current_element)
        children = []
        children.append(self.current_element)
        while ind > 0:
            ind -= 1
            prev_element = self.elements[ind]
            if prev_element.closed:
                children.append(prev_element)
                self.current_element.previous_sibling = prev_element
            else:
                self.current_element = prev_element
                self.current_element._children = children
                return

    def handle_data(self, data: str) -> None:
        data = data.strip()
        self.current_element.text += data
        self.current_element._all_text = self.current_element._all_text + [data]

    def find_all(self, tag: str, attrs: Optional[Dict[str, str | None]] = None, exclude_attrs: Optional[Dict[str, List[str | None]]] = None) -> List[HTMLElement]:
        """Return all matching elements"""
        return _find_all(self.elements, tag, attrs, exclude_attrs)

    def find(self, tag: str, attrs: Optional[Dict[str, str | None]] = None, exclude_attrs: Optional[Dict[str, List[str | None]]] = None) -> HTMLElement | None:
        """Return first matching element"""
        return _find(self.elements, tag, attrs, exclude_attrs)
