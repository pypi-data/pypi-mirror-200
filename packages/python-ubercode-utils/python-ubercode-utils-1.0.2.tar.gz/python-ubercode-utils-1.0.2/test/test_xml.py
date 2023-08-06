import unittest
from ubercode.utils.xml import XML
from pathlib import Path


class TestXML(unittest.TestCase):

    # -------- common usages ----------
    def test_XML(self):
        # calculate the filename for our test.xml file from this file (much like settings does)
        file_path = Path(__file__).resolve().parent / 'test.xml'
        xml_string = """
<contacts>
    <contact>
        <name>Steve Stacha</name>
    </contact>
    <contact>
        <name>Buggs Bunny</name>
    </contact>
    <contact>
        <name>Daffy Duck</name>
    </contact>
</contacts>
"""
        # test we can construct from an xml string
        xml = XML(xml_string=xml_string)
        # NOTE: because we used a multiline string we need to strip the extra newlines before and after <contacts>
        self.assertEqual(str(xml), xml_string.strip())
        # normal string doesn't need stripping
        xml_compact_string = "<contacts><contact><name>Buggs Bunny</name></contact><contact><name>Daffy Duck</name></contact></contacts>"
        xml2 = XML(xml_compact_string)
        self.assertEqual(str(xml2), xml_compact_string)
        # test we can create using the from_xml_string() method chaining
        xml3 = XML().from_xml_string(xml_compact_string)
        self.assertEqual(str(xml2), str(xml3))
        # test that method chaining after constructor overrides the value in place
        self.assertNotEqual(str(xml), str(xml2))
        xml.from_xml_string(xml_compact_string)
        self.assertEqual(str(xml), str(xml2))
        # test that we can read from file
        xml.from_xml_file(file_path)
        # we should be back to before
        self.assertEqual(str(xml), xml_string.strip())
        # test an attribute
        xml_string = """
<contacts>
    <contact attr="1">
        <name>Steve Stacha</name>
    </contact>
    <contact>
        <name>Buggs & Bunny</name>
    </contact>
    <contact>
        <name>Daffy Duck</name>
    </contact>
</contacts>
"""
        xml = XML(xml_string=xml_string, encode_ampersands=True)
        xml_dict = xml.to_dict()
        self.assertEqual(xml_dict['contacts']['contact'][0]['@attr'], '1')

