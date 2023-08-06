========================================
parselib - HTML parser for web scraping
========================================

.. code-block:: console
    
    pip install parselib

.. code-block:: python

    from parselib import Parser

    html = """
        <div class="class-one class-two">
            <div class="class-two">text</div>
        </div>
    """
    parser = Parser(html)
    div_one = parser.find("*", attrs={"class": "class-two class-one"})
    div_two = parser.find("*", attrs={"class": "class-two"}, exclude_attrs={"class": ["class-one"]})

----

find(tag, attrs=None, exclude_attrs=None)
    Return first matching element

find_all(tag, attrs=None, exclude_attrs=None)
    Return all matching elements

----

element.tagname
    Tag(str)

element.attrs
    Attributes(dict)
    
element.text
    Text

element.all_text
    All text within element

element.children
    Elements one level down

element.descendants
    All elements within element
    
element.parent
    Element one level up

element.next_sibling
    Next element on the same level

element.previous_sibling
    Previous element on the same level
