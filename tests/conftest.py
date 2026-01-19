#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
# Copyright (c) 2020 icecake0141

"""
Pytest configuration and fixtures
"""

import os
import sys
from unittest.mock import Mock, patch, MagicMock
import pytest

# Set environment variables before any imports
os.environ['SLACK_BOT_TOKEN'] = 'xoxb-test-token'
os.environ['SLACK_SIGNING_SECRET'] = 'test-secret'
os.environ['DEEPL_TOKEN'] = 'test-deepl-token'
os.environ['MULTI_CHANNEL'] = 'general'
os.environ['DEBUG_MODE'] = 'False'


def pytest_configure(config):
    """Pytest hook to set up mocks before any test collection"""
    # Mock Slack SDK auth_test to prevent real API calls
    auth_patcher = patch('slack_sdk.web.client.WebClient.auth_test')
    mock_auth = auth_patcher.start()
    mock_auth.return_value = {
        'ok': True,
        'url': 'https://test.slack.com/',
        'team': 'Test Team',
        'user': 'test_bot',
        'team_id': 'T12345',
        'user_id': 'U12345'
    }
    
    # Mock conversations_list to prevent real API calls
    # Return at least one channel so the loop in main.py runs and 'i' is defined
    conversations_patcher = patch('slack_sdk.web.client.WebClient.conversations_list')
    mock_conversations = conversations_patcher.start()
    mock_conversations.return_value = iter([{
        'channels': [
            {'id': 'C12345', 'name': 'general'},
            {'id': 'C67890', 'name': 'general-en'}
        ]
    }])
    
    # Store patchers for cleanup
    config._slack_patchers = [auth_patcher, conversations_patcher]


def pytest_unconfigure(config):
    """Pytest hook to clean up mocks after tests"""
    if hasattr(config, '_slack_patchers'):
        for patcher in config._slack_patchers:
            patcher.stop()
