from lxml import etree
from lxml.etree import Element
from datetime import datetime


def remove_xmlns(root):
    for elem in root.getiterator():
        elem.tag = etree.QName(elem).localname
    etree.cleanup_namespaces(root)


class CPObject(object):
    def make_ns(self, ns):
        return {
            "cp": ns
        }

    def val(self, data, xpath, ns=None):
        return self.elems(data, xpath)[0].text

    def text(self, node, name):
        sub_node = node.find(name)
        if sub_node:
            return sub_node.text
        else:
            return None

    def elems(self, data, xpath, ns=None):
        return data.xpath(xpath)

    def parse_xml(self, data):
        node = etree.fromstring(data)
        remove_xmlns(node)
        return node

    @classmethod
    def get_float(cls, node, xpath, ns=None):
        return float(node.find(xpath).text)

    def get_element(self):
        return Element(self._name)

    def __init__(self, **kw):
        self._allow_empty = False

        for key, value in kw.items():
            setattr(self, key, value)

    @classmethod
    def from_xml(cls, node):
        values = {}

        for key, field in cls._fields.items():
            values[key] = field.from_xml(node)

        return cls(**values)

    def to_xml(self, **kw):
        elem = self.get_element()

        if 'set_xmlns' in kw:
            kw = kw.copy()
            del kw['set_xmlns']
            xmlns = self._xmlns
        else:
            xmlns = None

        for key, field in self._fields.items():
            value = getattr(self, key, field.default)
            node = field.to_xml(value)

            if isinstance(node, list):
                for sub_node in node:
                    if sub_node is not None:
                        elem.append(sub_node)
            else:
                if node is not None:
                    elem.append(node)

        if xmlns:
            elem.attrib['xmlns'] = xmlns

        if (
            not xmlns and
            not self._allow_empty and
            not elem.text and
            len(elem.getchildren()) == 0
        ):
            return

        return elem


class BaseField(object):

    def __init__(
        self,
        name,
        property_name=None,
        format=None,
        default=None,
        allow_empty=False,
    ):
        self.name = name
        self.format = format
        self.property_name = property_name
        self.default = default
        self.allow_empty = allow_empty

    def to_xml(self, value):
        element = Element(self.name)

        f_value = self.format_value(value)

        if f_value is None and not self.allow_empty:
            return None

        element.text = str(f_value)

        return element

    def from_xml(self, node):
        if node is None:
            return self.default

        sub_node = node.find(self.name)
        if sub_node is None:
            return self.default
        return self.parse_value(sub_node)


text_formats = {
    "lowercase": lambda v: v.lower()
}


class TextField(BaseField):

    def format_value(self, value):
        if isinstance(self.format, str) and text_formats.get(self.format):
            f_value = text_formats.get(self.format)(value)
        elif callable(self.format):
            f_value = self.format(value)
        else:
            f_value = value

        return f_value

    def parse_value(self, node):
        return node.text


class BooleanField(BaseField):
    def format_value(self, value):
        if value is True:
            return 'true'
        elif value is False:
            return 'false'

    def parse_value(self, node):
        value = node.text

        if value == 'true':
            return True
        elif value == 'false':
            return False


class DateField(BaseField):

    def format_value(self, value):
        if value:
            return value.strftime(self.format)
        else:
            return self.default

    def parse_value(self, node):
        return datetime.strptime(node.text, self.format)


class ObjectField(BaseField):

    def to_xml(self, value):
        if not value:
            return
        return value.to_xml()

    def from_xml(self, node):
        node = node.find(self.name)
        if node is None:
            return
        return self.format.from_xml(node)


class LinksField(BaseField):

    def from_xml(self, node):
        # node = node.find('link[@rel="%s"]' % (self.name,))
        if node is not None:
            return {
                "href": node.attrib['href'],
                "media-type": node.attrib['media-type'],
                "rel": node.attrib['rel']
            }

    def to_xml(self, value):
        if not value:
            return

        elem = Element('link')
        elem.attrib['href'] = value['href']
        elem.attrib['media-type'] = value['media-type']
        elem.attrib['rel'] = value['rel']

        return elem


class LinkField(BaseField):

    def from_xml(self, node):
        node = node.find('link[@rel="%s"]' % (self.name,))
        if node is not None:
            return {
                "href": node.attrib['href'],
                "media-type": node.attrib['media-type'],
                "rel": node.attrib['rel']
            }

    def to_xml(self, value):
        if not value:
            return

        elem = Element('link')
        elem.attrib['href'] = value['href']
        elem.attrib['media-type'] = value['media-type']
        elem.attrib['rel'] = value['rel']

        return elem


class CollectionField(BaseField):
    def __init__(
        self,
        name,
        property_name=None,
        format=None,
        default=None,
        allow_empty=False,
        child_name=None,
        field_type=None
    ):
        super(CollectionField, self).__init__(
            name=name,
            property_name=property_name,
            format=format,
            default=default,
            allow_empty=allow_empty,
        )
        self.child_name = child_name
        self.field_type = field_type

    def to_xml(self, value):
        if not value:
            return None

        if self.format:
            nodes = [
                val.to_xml()
                for val in value
            ]
        elif self.field_type:
            if self.child_name:
                child_name = self.child_name
            else:
                child_name = self.name
            formatter = self.field_type(child_name)

            nodes = [
                formatter.to_xml(val)
                for val in value
            ]

        if not self.child_name:
            return nodes
        else:
            elem = Element(self.name)
            for node in nodes:
                if node is not None:
                    elem.append(node)
            return elem

    def from_xml(self, node):
        if node is None:
            return

        if self.child_name:
            child_name = self.child_name
            node = node.find(self.name)

            if node is None:
                return
        else:
            child_name = self.name

        if self.format:
            values = [
                self.format.from_xml(sub_node)
                for sub_node in node.xpath('.//%s' % (child_name))
                if sub_node is not None
            ]
        elif self.field_type:
            formatter = self.field_type(child_name)
            # TODO improve in a way that field can be reused without hacks
            # The main use was for loading
            # <option-code>a</option-code> as leaf values
            # but this also got used to load links collection which aren't
            # structured elements
            # so parse value doesn't exactly work
            try:
                values = [
                    formatter.parse_value(sub_node)
                    for sub_node in node.xpath('.//%s' % (child_name))
                    if sub_node is not None
                ]
            except Exception:
                values = [
                    formatter.from_xml(sub_node)
                    for sub_node in node.xpath('.//%s' % (child_name))
                    if sub_node is not None
                ]

        return values


class RangeField(BaseField):
    def from_xml(self, node):
        if node is None:
            return

        node = node.find(self.name)

        if node is None:
            return

        min_val = node.attrib.get('min', None)
        if min_val:
            min_val = float(min_val)

        max_val = node.attrib.get('max', None)
        if max_val:
            max_val = float(max_val)

        return {
            "min": min_val,
            "max": max_val
        }

    def to_xml(self, value):
        if not value:
            return
        elem = Element(self.name)

        if 'min' in value and value['min'] is not None:
            elem.attrib['min'] = str(value['min'])

        if 'max' in value and value['max'] is not None:
            elem.attrib['max'] = str(value['max'])

        return elem
