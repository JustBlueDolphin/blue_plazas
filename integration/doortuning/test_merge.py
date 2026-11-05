"""Small synthetic fixtures; no vendor tuning data is distributed."""
import unittest
import xml.etree.ElementTree as E
from merge import merge

FIXTURE=b'''<?xml version="1.0"?>
<CDoorTuningFile><!-- retain this vendor comment -->
<NamedTuningArray><Item><Name>DefaultStandard</Name><Tuning><Flags>DelayDoorClosingForPlayer</Flags><WeaponImpulseMultiplier value="1"/><VendorExtension value="keep"/></Tuning></Item></NamedTuningArray>
<ModelToTuneMapping><Item><ModelName>original_door</ModelName><TuningName>DefaultStandard</TuningName></Item></ModelToTuneMapping>
</CDoorTuningFile>'''

class MergeTests(unittest.TestCase):
    def test_add_and_idempotence(self):
        result,report=merge(FIXTURE)
        self.assertEqual(report['added_entries'],2)
        self.assertIn(b'<!-- retain this vendor comment -->',result)
        self.assertEqual(merge(result)[0],result)
        root=E.fromstring(result)
        self.assertEqual(len(root.findall('NamedTuningArray/Item')),2)
        self.assertEqual(root.findall('NamedTuningArray/Item')[1].find('Tuning/VendorExtension').get('value'),'keep')

    def test_partial_merge_adds_only_missing_mapping(self):
        result,_=merge(FIXTURE);root=E.fromstring(result)
        mappings=root.find('ModelToTuneMapping');mappings.remove(mappings[-1])
        self.assertEqual(merge(E.tostring(root))[1]['added_entries'],1)

    def test_conflicting_custom_profile_is_rejected(self):
        result,_=merge(FIXTURE);root=E.fromstring(result)
        root.findall('NamedTuningArray/Item')[1].find('Tuning/Flags').text='Different'
        with self.assertRaises(AssertionError):merge(E.tostring(root))

    def test_conflicting_model_mapping_is_rejected(self):
        result,_=merge(FIXTURE);root=E.fromstring(result)
        root.findall('ModelToTuneMapping/Item')[1].find('TuningName').text='DefaultStandard'
        with self.assertRaises(AssertionError):merge(E.tostring(root))

    def test_duplicate_custom_mapping_is_rejected(self):
        result,_=merge(FIXTURE);root=E.fromstring(result)
        mappings=root.find('ModelToTuneMapping');mappings.append(E.fromstring(E.tostring(mappings[-1])))
        with self.assertRaises(AssertionError):merge(E.tostring(root))

    def test_unresolved_reference_is_rejected(self):
        with self.assertRaises(AssertionError):merge(FIXTURE.replace(b'<TuningName>DefaultStandard',b'<TuningName>Missing'))

    def test_existing_vendor_duplicate_is_preserved(self):
        root=E.fromstring(FIXTURE);mappings=root.find('ModelToTuneMapping')
        mappings.append(E.fromstring(E.tostring(mappings[0])))
        result,report=merge(E.tostring(root))
        self.assertEqual(report['existing_duplicate_model_names'],['original_door'])
        self.assertEqual(len(E.fromstring(result).findall('ModelToTuneMapping/Item')),3)

    def test_crlf_preserved(self):
        original=FIXTURE.replace(b'\n',b'\r\n');result,_=merge(original)
        self.assertNotIn(b'\n',result.replace(b'\r\n',b''))

if __name__=='__main__':unittest.main()
