import unittest
from datetime import datetime
from unittest.mock import patch
from uuid import UUID

from pymisp import MISPAttribute, MISPEvent

from cyjax_misp.misp import Client, misp_org


class MISPEventMatcher(MISPEvent):
    def __eq__(self, other: MISPEvent):
        return self.info == other.info and self.Orgc == self.Orgc and self.date == self.date and self.analysis == other.analysis and self.published == other.published


class MISPAttributeMatcher(MISPAttribute):
    def __eq__(self, other: MISPAttribute):
        return self.type == other.type and self.value == self.value and self.timestamp == self.timestamp


class AnyClass:
    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, other):
        return isinstance(other, self.cls)


EVENT_UUID = '2c5cdb40-bb3f-4178-9fe9-998759cca32e'
INDICATOR_TIMESTAMP = '2020-12-07T08:42:54+0000'


@patch('pymisp.PyMISP')
class ClientTest(unittest.TestCase):

    def _create_misp_event(self, event_uuid: str, title: str, timestamp: str) -> MISPEvent:
        misp_event = MISPEventMatcher()
        misp_event.uuid = event_uuid
        misp_event.Orgc = misp_org
        misp_event.from_dict(info=title, date=timestamp, analysis=2, published=False)
        return misp_event

    def _create_misp_attribute(self, indicator_type: str, value: str, timestamp: str) -> MISPAttribute:
        attribute = MISPAttributeMatcher()
        attribute.from_dict(value=value, type=indicator_type,
                            timestamp=datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z'))
        return attribute

    def _create_indicator(self, indicator_type: str, value: str, source: str = None):
        return {
            'type': indicator_type,
            'value': value,
            'discovered_at': INDICATOR_TIMESTAMP,
            'source': source if source else 'https://cymon.com/incident/report/view?id=2334',
            'description': 'This is a test',
            'handling_condition': 'GREEN'
        }

    def test_save_indicator_with_new_event(self, pymisp_mock):
        self.client = Client('http://localhost:8888', 'test-misp-key')
        pymisp_mock.return_value.search.return_value = []
        self.client.save_indicator(self._create_indicator('Email', 'test@domain.com'))

        pymisp_mock.return_value.add_event.assert_called_with(
            self._create_misp_event(EVENT_UUID, 'This is a test',
                                    INDICATOR_TIMESTAMP))
        pymisp_mock.return_value.add_attribute.assert_called_with(AnyClass(str),
                                                                  self._create_misp_attribute('email-src',
                                                                                              'test@domain.com',
                                                                                              INDICATOR_TIMESTAMP))

    def test_save_indicator_with_existing_event(self, pymisp_mock):
        self.client = Client('http://localhost:8888', 'test-misp-key')
        pymisp_mock.return_value.search.return_value = [{'Event': {'uuid': EVENT_UUID}}]
        self.client.save_indicator(self._create_indicator('Email', 'test@domain.com'))

        pymisp_mock.return_value.add_event.assert_not_called()
        pymisp_mock.return_value.add_attribute.assert_called_with(EVENT_UUID,
                                                                  self._create_misp_attribute('email-src',
                                                                                              'test@domain.com',
                                                                                              INDICATOR_TIMESTAMP))

    def test_save_file_hash_md5_indicator(self, pymisp_mock):
        self._test_save_indicator(pymisp_mock, 'FileHash-MD5', 'md5', '098f6bcd4621d373cade4e832627b4f6')

    def test_save_file_hash_sha1_indicator(self, pymisp_mock):
        self._test_save_indicator(pymisp_mock, 'FileHash-SHA1', 'sha1', 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3')

    def test_save_file_hash_sha256_indicator(self, pymisp_mock):
        self._test_save_indicator(pymisp_mock, 'FileHash-SHA256', 'sha256', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08')

    def test_save_file_hash_ssdeep_indicator(self, pymisp_mock):
        self._test_save_indicator(pymisp_mock, 'FileHash-SSDEEP', 'ssdeep', '96:s4Ud1Lj96tHHlZDrwciQmA+4uy1I0G4HYuL8N3TzS8QsO/wqWXLcMSx:sF1LjEtHHlZDrJzrhuyZvHYm8tKp/RWO')

    def test_save_ipv4_indicator(self, pymisp_mock):
        self._test_save_indicator(pymisp_mock, 'IPv4', 'ip-src', '10.1.1.1')

    def test_save_ipv6_indicator(self, pymisp_mock):
        self._test_save_indicator(pymisp_mock, 'IPv6', 'ip-src', '::1')

    def test_save_url_indicator(self, pymisp_mock):
        self._test_save_indicator(pymisp_mock, 'URL', 'url', 'http://test.com')

    def test_save_hostname_indicator(self, pymisp_mock):
        self._test_save_indicator(pymisp_mock, 'Hostname', 'hostname', 'foobar.test.com')

    def test_save_domain_indicator(self, pymisp_mock):
        self._test_save_indicator(pymisp_mock, 'Domain', 'domain', 'test.com')

    def test_save_indicator_with_new_url_format(self, pymisp_mock):
        self.client = Client('http://localhost:8888', 'test-misp-key', 'https://cymon.com/incident/report/2334')
        pymisp_mock.return_value.search.return_value = []
        self.client.save_indicator(self._create_indicator('Email', 'test@domain.com'))

        pymisp_mock.return_value.add_event.assert_called_with(
            self._create_misp_event(EVENT_UUID, 'This is a test',
                                    INDICATOR_TIMESTAMP))
        pymisp_mock.return_value.add_attribute.assert_called_with(AnyClass(str),
                                                                  self._create_misp_attribute('email-src',
                                                                                              'test@domain.com',
                                                                                              INDICATOR_TIMESTAMP))

    def _test_save_indicator(self, pymisp_mock, indicator_type, misp_indicator_type, indicator_value):
        self.client = Client('http://localhost:8888', 'test-misp-key')
        pymisp_mock.return_value.search.return_value = [{'Event': {'uuid': EVENT_UUID}}]

        self.client.save_indicator(self._create_indicator(indicator_type, indicator_value))

        pymisp_mock.return_value.add_event.assert_not_called()
        pymisp_mock.return_value.add_attribute.assert_called_with(EVENT_UUID,
                                                                  self._create_misp_attribute(misp_indicator_type,
                                                                                              indicator_value,
                                                                                              INDICATOR_TIMESTAMP))
