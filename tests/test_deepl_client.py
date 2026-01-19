#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
# Copyright (c) 2020 icecake0141
# This file contains LLM-generated code that has been reviewed and approved by humans.

"""
Unit tests for deepl_client module
"""

import pytest
import requests
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path to import deepl_client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import deepl_client


class TestTranslateText:
    """Test cases for translate_text function"""

    @patch("requests.Session.post")
    def test_translate_text_success(self, mock_post):
        """Test successful translation"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "translations": [{"detected_source_language": "EN", "text": "こんにちは"}]
        }
        mock_post.return_value = mock_response

        result = deepl_client.translate_text("test-key", "Hello", "JA")

        assert result == "こんにちは"
        assert mock_post.called

        # Verify correct parameters were used
        call_args = mock_post.call_args
        assert call_args[1]["data"]["text"] == "Hello"
        assert call_args[1]["data"]["target_lang"] == "JA"
        assert call_args[1]["data"]["tag_handling"] == "xml"
        assert call_args[1]["timeout"] == 10

    @patch("requests.Session.post")
    def test_translate_text_custom_timeout(self, mock_post):
        """Test translation with custom timeout"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"translations": [{"text": "Bonjour"}]}
        mock_post.return_value = mock_response

        deepl_client.translate_text("test-key", "Hello", "FR", timeout=30)

        # Verify timeout parameter
        call_args = mock_post.call_args
        assert call_args[1]["timeout"] == 30

    @patch("requests.Session.post")
    def test_translate_text_http_error(self, mock_post):
        """Test translation with HTTP error response"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_post.return_value = mock_response

        with pytest.raises(deepl_client.DeeplClientError) as exc_info:
            deepl_client.translate_text("invalid-key", "Hello", "JA")

        assert "HTTP error" in str(exc_info.value)

    @patch("requests.Session.post")
    def test_translate_text_timeout(self, mock_post):
        """Test translation with timeout error"""
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

        with pytest.raises(deepl_client.DeeplClientError) as exc_info:
            deepl_client.translate_text("test-key", "Hello", "JA")

        assert "timed out" in str(exc_info.value).lower()

    @patch("requests.Session.post")
    def test_translate_text_invalid_json(self, mock_post):
        """Test translation with malformed JSON response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"invalid": "structure"}
        mock_post.return_value = mock_response

        with pytest.raises(deepl_client.DeeplClientError) as exc_info:
            deepl_client.translate_text("test-key", "Hello", "JA")

        assert "Invalid response" in str(exc_info.value)

    @patch("requests.Session.post")
    def test_translate_text_empty_translations(self, mock_post):
        """Test translation with empty translations array"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"translations": []}
        mock_post.return_value = mock_response

        with pytest.raises(deepl_client.DeeplClientError) as exc_info:
            deepl_client.translate_text("test-key", "Hello", "JA")

        assert "Invalid response" in str(exc_info.value)

    @patch("requests.Session.post")
    def test_translate_text_network_error(self, mock_post):
        """Test translation with network error"""
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")

        with pytest.raises(deepl_client.DeeplClientError) as exc_info:
            deepl_client.translate_text("test-key", "Hello", "JA")

        assert "Request failed" in str(exc_info.value)

    @patch("requests.Session.post")
    def test_translate_text_with_tags(self, mock_post):
        """Test translation preserves tag_handling parameter"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "translations": [{"text": "Translated <tag>text</tag>"}]
        }
        mock_post.return_value = mock_response

        result = deepl_client.translate_text("test-key", "Some <tag>text</tag>", "EN")

        # Verify tag_handling is set to xml
        call_args = mock_post.call_args
        assert call_args[1]["data"]["tag_handling"] == "xml"
        assert result == "Translated <tag>text</tag>"


class TestGetUsage:
    """Test cases for get_usage function"""

    @patch("requests.Session.post")
    def test_get_usage_success(self, mock_post):
        """Test successful usage retrieval"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "character_count": 12345,
            "character_limit": 500000,
        }
        mock_post.return_value = mock_response

        count, limit = deepl_client.get_usage("test-key")

        assert count == 12345
        assert limit == 500000
        assert mock_post.called

    @patch("requests.Session.post")
    def test_get_usage_custom_timeout(self, mock_post):
        """Test usage retrieval with custom timeout"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "character_count": 1000,
            "character_limit": 100000,
        }
        mock_post.return_value = mock_response

        deepl_client.get_usage("test-key", timeout=20)

        # Verify timeout parameter
        call_args = mock_post.call_args
        assert call_args[1]["timeout"] == 20

    @patch("requests.Session.post")
    def test_get_usage_http_error(self, mock_post):
        """Test usage retrieval with HTTP error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_post.return_value = mock_response

        with pytest.raises(deepl_client.DeeplClientError) as exc_info:
            deepl_client.get_usage("invalid-key")

        assert "HTTP error" in str(exc_info.value)

    @patch("requests.Session.post")
    def test_get_usage_timeout(self, mock_post):
        """Test usage retrieval with timeout"""
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

        with pytest.raises(deepl_client.DeeplClientError) as exc_info:
            deepl_client.get_usage("test-key")

        assert "timed out" in str(exc_info.value).lower()

    @patch("requests.Session.post")
    def test_get_usage_invalid_response(self, mock_post):
        """Test usage retrieval with invalid response structure"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"invalid": "data"}
        mock_post.return_value = mock_response

        with pytest.raises(deepl_client.DeeplClientError) as exc_info:
            deepl_client.get_usage("test-key")

        assert "Invalid response" in str(
            exc_info.value
        ) or "missing usage fields" in str(exc_info.value)

    @patch("requests.Session.post")
    def test_get_usage_missing_character_count(self, mock_post):
        """Test usage retrieval with missing character_count"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"character_limit": 500000}
        mock_post.return_value = mock_response

        with pytest.raises(deepl_client.DeeplClientError):
            deepl_client.get_usage("test-key")

    @patch("requests.Session.post")
    def test_get_usage_missing_character_limit(self, mock_post):
        """Test usage retrieval with missing character_limit"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"character_count": 12345}
        mock_post.return_value = mock_response

        with pytest.raises(deepl_client.DeeplClientError):
            deepl_client.get_usage("test-key")

    @patch("requests.Session.post")
    def test_get_usage_network_error(self, mock_post):
        """Test usage retrieval with network error"""
        mock_post.side_effect = requests.exceptions.ConnectionError(
            "Network unreachable"
        )

        with pytest.raises(deepl_client.DeeplClientError) as exc_info:
            deepl_client.get_usage("test-key")

        assert "Request failed" in str(exc_info.value)


class TestDeeplClientError:
    """Test cases for DeeplClientError exception"""

    def test_exception_can_be_raised(self):
        """Test that DeeplClientError can be raised and caught"""
        with pytest.raises(deepl_client.DeeplClientError):
            raise deepl_client.DeeplClientError("Test error")

    def test_exception_message(self):
        """Test that exception message is preserved"""
        error_msg = "Custom error message"
        try:
            raise deepl_client.DeeplClientError(error_msg)
        except deepl_client.DeeplClientError as e:
            assert str(e) == error_msg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
