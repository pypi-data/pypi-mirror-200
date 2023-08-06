"""
A collection of basic xml conversion helper utilities.
"""
import xml.etree.ElementTree as Etree
import re
# from typing import Self (Not available until 3.9; omitting for now)
from collections import defaultdict


class XML:
    """ simple xml class to encapsulate basic xml operations """
    # the base implementation will be Etree from the base python lib
    xml_tree = None

    def __init__(self, xml_string: str or None = None, encode_ampersands: bool = False):
        self.encode_ampersands = encode_ampersands
        self.from_xml_string(xml_string)

    def from_xml_string(self, xml_string: str):
        """
        read in from xml_string
        :param xml_string:
        :return: self
        """
        if xml_string:
            if self.encode_ampersands:
                regex = re.compile(r"&(?!amp;|lt;|gt;)")
                xml_string = regex.sub("&amp;", xml_string)
            self.xml_tree = Etree.fromstring(xml_string)
        return self

    def from_xml_file(self, xml_file_path: str):
        """
        read in from xml_file
        :param xml_file_path:
        :return: self
        """
        # if we need to encode load the file replace and then load the etree from string
        if self.encode_ampersands:
            # note: encoding was utf-8-sig
            with open(xml_file_path, encoding='utf-8') as xml_file:
                xml_string = xml_file.read()
                regex = re.compile(r"&(?!amp;|lt;|gt;)")
                xml_string = regex.sub("&amp;", xml_string)
                tree = Etree.fromstring(xml_string)
        else:
            tree = Etree.parse(xml_file_path)
            tree = tree.getroot()
        self.xml_tree = tree
        return self

    def to_dict(self) -> dict:
        """
        output to dict
        :return: dict
        """
        return XML.tree_to_dict(self.xml_tree)

    @staticmethod
    def tree_to_dict(t) -> dict:
        """
        Convert an etree structure to a dictionary of values
        :param t: etree instance
        :return: dictionary of values
        """
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(XML.tree_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                    d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d

    def __str__(self):
        if self.xml_tree:
            return Etree.tostring(self.xml_tree, encoding='unicode')
        return ""
