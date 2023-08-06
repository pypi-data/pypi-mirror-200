"""This module provides CLI commands."""

import sys
from datetime import timedelta, datetime
import logging

import cyjax
import pytz
from cyjax import ResponseErrorException, IndicatorOfCompromise, ApiKeyNotFoundException
from cyjax.exceptions import TooManyRequestsException

from cyjax_misp import misp
from cyjax_misp.configuration import Configuration, InvalidConfigurationException

log = logging.getLogger('cyjax-misp')


configuration = Configuration()
configuration.load()


def setup_misp_module():
    """Sets the MISP module up."""
    print('=== MISP input module for Cyjax Threat Intelligence platform ===\n')

    cyjax_api_key = input('Please provide the Cyjax API key:')
    misp_url = input('Please provide the MISP URL:')
    misp_api_key = input('Please provide the MISP API key:')

    try:
        configuration.set_config(cyjax_api_key, misp_url, misp_api_key)
        print("Configuration saved to %s" % (configuration.get_config_file_path()))
    except InvalidConfigurationException as exception:
        print('Error: {}'.format(str(exception)))


def run_misp_module(debug: bool = False):
    """Runs the MISP module.
    :param debug: Whether to enable debug.
    """
    try:
        configuration.validate()
    except InvalidConfigurationException:
        log.error('Please configure the MISP input module with --setup argument.')
        sys.exit(-1)

    misp_client = misp.Client(configuration.get_misp_url(), configuration.get_misp_api_key(), debug)

    log.info("Running MISP input module...")
    log.info("Using configuration file %s", configuration.get_config_file_path())
    added_indicator_count = 0
    try:
        last_sync_timestamp = configuration.get_last_sync_timestamp()
        if isinstance(last_sync_timestamp, timedelta):
            last_sync_timestamp = datetime.now(tz=pytz.UTC) - last_sync_timestamp
        log.info("Checking indicators since %s", last_sync_timestamp)

        new_sync_timestamp = datetime.now(tz=pytz.UTC)
        cyjax.api_key = configuration.get_cyjax_api_key()
        for indicator in IndicatorOfCompromise().list(since=configuration.get_last_sync_timestamp()):
            added_indicator_count += 1
            log.debug("Processing indicator %s (%s)", indicator['value'], indicator['type'])
            misp_client.save_indicator(indicator)

        configuration.save_last_sync_timestamp(new_sync_timestamp)
        log.info("Added %s indicators", added_indicator_count)
    except ResponseErrorException:
        log.error("Error fetching indicators")
    except ApiKeyNotFoundException:
        log.error("Please setup an API key")
    except TooManyRequestsException:
        log.error("Rate limit exceeded")
