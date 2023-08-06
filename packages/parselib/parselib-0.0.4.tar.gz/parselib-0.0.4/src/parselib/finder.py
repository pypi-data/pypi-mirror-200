def _find_all(elements, tag: str, attrs=None, exclude_attrs=None):
    results = []
    for el in elements:
        if tag != "*" and el.tagname != tag:
            continue
        if attrs and not el.attrs:
            continue
        if attributes_allowed(el.attrs, attrs, exclude_attrs):
            results.append(el)
    return results


def _find(elements, tag: str, attrs=None, exclude_attrs=None):
    for el in elements:
        if tag != "*" and el.tagname != tag:
            continue
        if attrs and not el.attrs:
            continue
        if attributes_allowed(el.attrs, attrs, exclude_attrs):
            return el
    return None


def attributes_allowed(element_attrs, include_attrs, exclude_attrs):
    if include_attrs:
        for k, v in include_attrs.items():
            if k == "class":
                if "class" not in element_attrs.keys():
                    return False
                if element_attrs.get("class") == v:
                    continue
                if v == None:
                    return False
                element_classes = element_attrs.get("class").split(" ")
                for cls in v.split(" "):
                    if cls not in element_classes:
                        return False
                continue
            if k not in element_attrs.keys():
                return False
            if element_attrs.get(k) != v:
                return False
    if not element_attrs:
        return True
    if exclude_attrs:
        for k, v in exclude_attrs.items():
            if k == "class":
                if "class" not in element_attrs.keys():
                    continue
                element_classes = element_attrs.get("class")
                if element_classes in v:
                    return False
                if element_classes == None:
                    continue
                element_classes = element_classes.split(" ")
                for cls in v:
                    if cls in element_classes:
                        return False
                continue
            if k not in element_attrs.keys():
                continue
            element_val = element_attrs.get(k)
            for exclude_val in v:
                if exclude_val == element_val:
                    return False
    return True
