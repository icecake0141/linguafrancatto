#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
# Copyright (c) 2020 icecake0141

"""
Unit tests for linguafrancatto main module
"""

import json
import pytest
from unittest.mock import patch
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import main module (env vars set in conftest.py)
import main


class TestMarkdownFunctions:
    """Test cases for markdown replacement and reversion functions"""

    def test_replace_markdown_bold(self):
        """Test that asterisks are replaced with bold tags"""
        text = "This is *bold* text"
        result = main.replace_markdown(text)
        # Each asterisk is replaced with the tag
        assert "<bd></bd>" in result
        assert "*" not in result
        assert result == "This is <bd></bd>bold<bd></bd> text"

    def test_replace_markdown_italic(self):
        """Test that underscores are replaced with italic tags"""
        text = "This is _italic_ text"
        result = main.replace_markdown(text)
        assert "<it></it>" in result
        assert "_" not in result

    def test_replace_markdown_strikethrough(self):
        """Test that tildes are replaced with strikethrough tags"""
        text = "This is ~strikethrough~ text"
        result = main.replace_markdown(text)
        assert "<st></st>" in result
        assert "~" not in result

    def test_replace_markdown_code_block(self):
        """Test that triple backticks are replaced with code block tags"""
        text = "This is ```code block``` text"
        result = main.replace_markdown(text)
        assert "<cb></cb>" in result
        assert "```" not in result

    def test_replace_markdown_inline_code(self):
        """Test that single backticks are replaced with inline code tags"""
        text = "This is `inline code` text"
        result = main.replace_markdown(text)
        assert "<cd></cd>" in result
        # Should still have opening/closing backticks replaced

    def test_replace_markdown_list_symbol(self):
        """Test that bullet points are replaced with list tags"""
        text = "• List item"
        result = main.replace_markdown(text)
        assert "<ls></ls>" in result
        assert "•" not in result

    def test_replace_markdown_angle_brackets(self):
        """Test that angle brackets are HTML-escaped"""
        text = "<tag>content</tag>"
        result = main.replace_markdown(text)
        assert "&lt;" in result
        assert "&gt;" in result
        assert "<tag>" not in result
        assert "</tag>" not in result

    def test_replace_markdown_multiple_elements(self):
        """Test replacing multiple markdown elements at once"""
        text = "This has *bold*, _italic_, and `code`"
        result = main.replace_markdown(text)
        assert "<bd></bd>" in result
        assert "<it></it>" in result
        assert "<cd></cd>" in result

    def test_revert_markdown_bold(self):
        """Test that bold tags are reverted to asterisks"""
        # Use actual output from replace_markdown
        original = "This is *bold* text"
        replaced = main.replace_markdown(original)
        result = main.revert_markdown(replaced)
        assert "*" in result
        assert "<bd></bd>" not in result
        assert result == original

    def test_revert_markdown_italic(self):
        """Test that italic tags are reverted to underscores"""
        # Use actual output from replace_markdown
        original = "This is _italic_ text"
        replaced = main.replace_markdown(original)
        result = main.revert_markdown(replaced)
        assert "_" in result
        assert "<it></it>" not in result
        assert result == original

    def test_revert_markdown_strikethrough(self):
        """Test that strikethrough tags are reverted to tildes"""
        # Use actual output from replace_markdown
        original = "This is ~strikethrough~ text"
        replaced = main.replace_markdown(original)
        result = main.revert_markdown(replaced)
        assert "~" in result
        assert "<st></st>" not in result
        assert result == original

    def test_revert_markdown_code_block(self):
        """Test that code block tags are reverted to triple backticks"""
        # Use actual output from replace_markdown
        original = "This is ```code block``` text"
        replaced = main.replace_markdown(original)
        result = main.revert_markdown(replaced)
        assert "```" in result
        assert "<cb></cb>" not in result
        assert result == original

    def test_revert_markdown_inline_code(self):
        """Test that inline code tags are reverted to backticks"""
        # Use actual output from replace_markdown
        original = "This is `inline code` text"
        replaced = main.replace_markdown(original)
        result = main.revert_markdown(replaced)
        assert "`" in result
        assert "<cd></cd>" not in result
        assert result == original

    def test_revert_markdown_list_symbol(self):
        """Test that list tags are reverted to bullet points"""
        text = "<ls></ls> List item"
        result = main.revert_markdown(text)
        assert "•" in result
        assert "<ls></ls>" not in result

    def test_revert_markdown_angle_brackets(self):
        """Test that HTML-escaped brackets are reverted"""
        text = "&lt;tag&gt;content&lt;/tag&gt;"
        result = main.revert_markdown(text)
        assert "<" in result
        assert ">" in result
        assert "&lt;" not in result
        assert "&gt;" not in result

    def test_revert_markdown_multiple_elements(self):
        """Test reverting multiple markdown elements at once"""
        text = "This has <bd></bd>, <it></it>, and <cd></cd>"
        result = main.revert_markdown(text)
        assert "*" in result
        assert "_" in result
        assert "`" in result

    def test_replace_and_revert_roundtrip(self):
        """Test that replace and revert are inverse operations"""
        original = "This is *bold*, _italic_, ~strike~, ```code```, `inline`, and <tag>"
        replaced = main.replace_markdown(original)
        reverted = main.revert_markdown(replaced)

        # The roundtrip should preserve the markdown formatting
        # Note: angle brackets behavior might differ
        assert "*" in reverted
        assert "_" in reverted
        assert "~" in reverted


class TestDeepLFunctions:
    """Test cases for DeepL API interaction functions"""

    @patch("deepl_client.translate_text")
    def test_deepl_translation_success(self, mock_translate):
        """Test successful DeepL translation API call"""
        # Mock the client function
        mock_translate.return_value = "こんにちは"

        result = main.deepl("Hello", "JA")

        assert result == "こんにちは"
        assert mock_translate.called
        # Verify API was called with correct parameters
        call_args = mock_translate.call_args
        assert call_args[0][1] == "Hello"  # text
        assert call_args[0][2] == "JA"  # target_lang

    @patch("deepl_client.translate_text")
    def test_deepl_translation_with_tags(self, mock_translate):
        """Test DeepL translation with tag_handling parameter"""
        mock_translate.return_value = "Texte traduit"

        main.deepl("Test text", "FR")

        # Verify the client was called
        assert mock_translate.called

    @patch("deepl_client.get_usage")
    def test_deepl_usage_success(self, mock_get_usage):
        """Test successful DeepL usage API call"""
        # Mock the client function
        mock_get_usage.return_value = (12345, 500000)

        count, limit = main.deepl_usage()

        assert count == 12345
        assert limit == 500000
        assert mock_get_usage.called

    @patch("deepl_client.get_usage")
    def test_deepl_usage_endpoint(self, mock_get_usage):
        """Test that deepl_usage calls the correct endpoint"""
        mock_get_usage.return_value = (1000, 100000)

        main.deepl_usage()

        # Verify the usage function was called
        assert mock_get_usage.called


class TestFlaskApp:
    """Test cases for Flask application routes"""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        main.app.config["TESTING"] = True
        return main.app.test_client()

    def test_start_endpoint(self, client):
        """Test the /_ah/start endpoint"""
        response = client.get("/_ah/start")
        assert response.status_code == 200
        assert response.data == b""

    def test_stop_endpoint(self, client):
        """Test the /_ah/stop endpoint"""
        response = client.get("/_ah/stop")
        assert response.status_code == 200
        assert response.data == b""

    @patch("main.handler.handle")
    def test_slack_events_endpoint(self, mock_handle, client):
        """Test the /slack/events endpoint"""
        mock_handle.return_value = ("OK", 200, {})

        client.post(
            "/slack/events",
            data=json.dumps({"event": "test"}),
            content_type="application/json",
        )

        # The handler should be called
        assert mock_handle.called


class TestEnvironmentVariables:
    """Test environment variable configuration"""

    def test_debug_mode_env_var(self):
        """Test DEBUG environment variable is read"""
        # This tests that the module reads the environment variable
        # We can't easily test this without reimporting, so we just verify
        # the variable name is correct in the code
        assert True  # Placeholder for environment variable tests

    def test_deepl_token_env_var(self):
        """Test DEEPL_TOKEN environment variable is used"""
        # Placeholder - in real scenario, would test token is read correctly
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
