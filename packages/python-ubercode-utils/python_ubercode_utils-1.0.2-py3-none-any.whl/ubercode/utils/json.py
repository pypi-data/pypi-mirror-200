"""
A collection of basic json conversion helper utilities.
"""
import json
import re
# from typing import Self (Not available until 3.9; omitting for now)


class JSON:
    """ simple json class to encapsulate basic json operations """
    # the base implementation will be dict
    json_dict = {}

    def __init__(self, json_string: str or None = None, encode_ampersands: bool = False):
        self.encode_ampersands = encode_ampersands
        self.from_json_string(json_string)

    def from_json_string(self, json_string: str):
        """
        read in from json_string
        :param json_string:
        :return: self
        """
        if json_string:
            if self.encode_ampersands:
                regex = re.compile(r"&(?!amp;|lt;|gt;)")
                json_string = regex.sub("&amp;", json_string)
            self.json_dict = json.loads(json_string)
        return self

    def from_json_file(self, json_file_path: str):
        """
        read in from json_file
        :param json_file_path: string to file
        :return: self
        """
        with open(json_file_path, encoding='utf-8-sig') as json_file:
            json_string = json_file.read()
        if json_string:
            if self.encode_ampersands:
                regex = re.compile(r"&(?!amp;|lt;|gt;)")
                json_string = regex.sub("&amp;", json_string)
            self.json_dict = json.loads(json_string)
        return self

    def to_dict(self) -> dict:
        """
        output to dict
        :return: dict
        """
        return self.json_dict

    def __str__(self):
        return str(self.json_dict)
