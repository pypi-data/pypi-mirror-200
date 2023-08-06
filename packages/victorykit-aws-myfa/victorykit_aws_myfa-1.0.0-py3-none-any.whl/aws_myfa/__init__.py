#!/usr/bin/env python3
"""Create and maintain AWS CLI profiles requiring MFA-authenticated STS sessions
with ease.
"""
from configparser import ConfigParser
from dataclasses import dataclass, field, asdict
from os import environ
from pathlib import Path
import json
from sys import exit, stdout
from subprocess import check_output
from typing import Dict, Optional


class NoSuchProfileException(Exception):
    """An exception when an AWS CLI profile does not exist
    """


class NoSuchSourceProfileException(NoSuchProfileException):
    """An exception when an AWS CLI source profile does not exist
    """


@dataclass
class Context:
    """main program configuration
    """

    #: path to AWS CLI credentials (default: ~/.aws/credentials)
    credentials_path: Path

    #: path to AWS CLI config (default: ~/.aws/config)
    config_path: Path

    #: the ARN under which your virtual MFA device is registered
    mfa_device_arn: str

    acknowledge_prompts: Optional[bool] = False

    #: a token code from your virtual MFA device
    mfa_token_code: Optional[str] = ''

    #: path to AWS CLI credentials (default: ~/.aws/credentials)
    profile_names: Dict[str, str] = field(default_factory= {
        'session': '',
        'principal': '',
    })

    #: path to AWS CLI credentials (default: ~/.aws/credentials)
    session_profile_name: Optional[str] = 'default'


@dataclass
class Profile:
    """abstract AWS CLI profile
    """

    name: str

    region: str

    output: Optional[str] = 'json'

    source_profile: Optional[str] = 'default'

    account: Optional[str] = None


@dataclass
class SourceProfile:
    """abstract AWS CLI source profile
    """
    name: str

    aws_access_key_id: str

    aws_secret_access_key: str

    aws_session_token: Optional[str] = ''

    aws_mfa_device_arn: Optional[str] = ''

    expiration: Optional[str] = ''


def get_profile(
    name: str,
    config: ConfigParser,
) -> Profile:
    """get an AWS CLI profile from a parsed AWS CLI config file
    """

    assertion_message = f"{name}: no profile with such a name"

    if name == 'default':

        try:

            assert 'default' in config.sections(), assertion_message

        except AssertionError as err:

            raise NoSuchProfileException(err) from err
    else:

        section_prefix = 'profile'

        profile_names = [s.split(' ', 1)[1] for s in config.sections() if s[:len(section_prefix)] == section_prefix]

        try:

            assert name in profile_names, assertion_message

        except AssertionError as err:

            raise NoSuchProfileException(err) from err

    section_name = name

    if name != 'default':

        section_name = f"profile {name}"

    return Profile(**{**dict(config[section_name]), **{'name': name}})


def get_source_profile(
    name: str,
    config: ConfigParser
) -> SourceProfile:
    """get an AWS CLI profile from a parsed AWS CLI config file
    """
    try:

        assert name in config.sections(), f"{name}: source profile does not exist"
    except AssertionError as err:

        raise NoSuchSourceProfileException(err) from err

    return SourceProfile(**{**dict(config[name]), **{'name': name}})


def get_session_source_profile(
    name: str,
    mfa_device_arn: str,
    mfa_token_code: str,
    env: Dict,
) -> SourceProfile:
    """
    """

    cmd = [
        'aws',
        'sts',
        'get-session-token',
        '--serial-number',
        mfa_device_arn,
        '--token-code',
        mfa_token_code,
        '--output', 'json',
        '--profile', env['AWS_PROFILE']
    ]

    print("\033[94m%s\033[0m" % ' '.join(cmd))

    credentials = json.loads(check_output(cmd, env=env)).get('Credentials')

    return SourceProfile(
        name = name,
        aws_access_key_id = credentials.get('AccessKeyId'),
        aws_secret_access_key = credentials.get('SecretAccessKey'),
        aws_session_token = credentials.get('SessionToken'),
        aws_mfa_device_arn = mfa_device_arn,
        expiration = credentials.get('Expiration')
    )