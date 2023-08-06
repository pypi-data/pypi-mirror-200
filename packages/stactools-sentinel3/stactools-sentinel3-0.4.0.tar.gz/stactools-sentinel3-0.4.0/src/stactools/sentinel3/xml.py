from stactools.core.io.xml import XmlElement


def find_text(xml_element: XmlElement, xpath: str) -> str:
    def raise_exception(message: str) -> Exception:
        return Exception(f"could not find xpath {xpath}: {message}")

    text = xml_element.find_or_throw(xpath, raise_exception).text
    if text is None:
        raise Exception(f"xpath {xpath} does not have any text")
    else:
        return text
