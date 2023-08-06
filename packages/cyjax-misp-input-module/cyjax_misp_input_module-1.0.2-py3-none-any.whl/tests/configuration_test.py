import unittest

from cyjax_misp.configuration import Configuration, CYJAX_API_KEY, MISP_URL, MISP_API_KEY, \
    InvalidConfigurationException, CONFIG_FILE_PATH


class ConfigurationTest(unittest.TestCase):
    def setUp(self):
        self.configuration = Configuration()
        self.configuration.config[CYJAX_API_KEY] = 'test-cyjax-key'
        self.configuration.config[MISP_URL] = 'http://misp-url.com'
        self.configuration.config[MISP_API_KEY] = 'test-misp-key'

    def test_validate_with_no_cyjax_key(self):
        del self.configuration.config[CYJAX_API_KEY]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Cyjax API key cannot be empty.', str(context.exception))

    def test_validate_with_empty_cyjax_key(self):
        self.configuration.config[CYJAX_API_KEY] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Cyjax API key cannot be empty.', str(context.exception))

    def test_validate_with_no_misp_url(self):
        del self.configuration.config[MISP_URL]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The MISP URL cannot be empty.', str(context.exception))

    def test_validate_with_empty_misp_url(self):
        self.configuration.config[MISP_URL] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The MISP URL cannot be empty.', str(context.exception))

    def test_validate_with_no_misp_key(self):
        del self.configuration.config[MISP_API_KEY]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The MISP API key cannot be empty.', str(context.exception))

    def test_validate_with_empty_misp_key(self):
        self.configuration.config[MISP_API_KEY] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The MISP API key cannot be empty.', str(context.exception))

    def test_get_cyjax_api_key(self):
        self.assertEqual('test-cyjax-key', self.configuration.get_cyjax_api_key())

    def test_get_misp_url(self):
        self.assertEqual('http://misp-url.com', self.configuration.get_misp_url())

    def test_get_misp_api_key(self):
        self.assertEqual('test-misp-key', self.configuration.get_misp_api_key())

    def test_get_config_file_path(self):
        self.configuration.config_file_path = '/test/' + CONFIG_FILE_PATH
        self.assertEqual('/test/' + CONFIG_FILE_PATH, self.configuration.get_config_file_path())
