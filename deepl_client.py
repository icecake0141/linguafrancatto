#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
# Copyright (c) 2020 icecake0141
# This file contains LLM-generated code that has been reviewed and approved by humans.

"""
DeepL API client with robust error handling, timeouts, and retries.

This module provides functions to interact with the DeepL translation API
with proper error handling, connection timeouts, and retry logic.
"""

import logging
import requests
from typing import Tuple
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class DeeplClientError(Exception):
    """
    Custom exception for DeepL API client errors.

    This exception is raised when there are issues communicating with
    the DeepL API, including network errors, timeouts, or invalid responses.
    """

    pass


def translate_text(
    auth_key: str, text: str, target_lang: str, timeout: int = 10
) -> str:
    """
    Translate text using the DeepL API with robust error handling.

    Args:
        auth_key: DeepL API authentication key
        text: Text to translate
        target_lang: Target language code (e.g., 'EN', 'FR', 'JA')
        timeout: Request timeout in seconds (default: 10)

    Returns:
        Translated text as a string

    Raises:
        DeeplClientError: If the API request fails or returns invalid data
    """
    url = "https://api.deepl.com/v2/translate"

    # Configure retry strategy for network resilience
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )

    # Create session with retry adapter
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)

    # Prepare headers (avoid logging auth_key)
    headers = {"User-Agent": "linguafrancatto/2.1"}

    # Prepare form data
    data = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_lang,
        "tag_handling": "xml",
    }

    try:
        # Make POST request with form-encoded data
        response = session.post(url, data=data, headers=headers, timeout=timeout)
        response.raise_for_status()

        # Parse JSON response
        result = response.json()

        # Extract translated text
        if "translations" not in result or len(result["translations"]) == 0:
            logging.error("DeepL API returned invalid response structure")
            raise DeeplClientError(
                "Invalid response from DeepL API: missing translations"
            )

        translated_text = result["translations"][0]["text"]
        return translated_text

    except requests.exceptions.Timeout as e:
        logging.error("DeepL API request timed out")
        raise DeeplClientError(f"Request timed out: {str(e)}") from e
    except requests.exceptions.HTTPError as e:
        logging.error(f"DeepL API HTTP error: {e.response.status_code}")
        raise DeeplClientError(f"HTTP error: {e.response.status_code}") from e
    except requests.exceptions.RequestException as e:
        logging.error(f"DeepL API request failed: {type(e).__name__}")
        raise DeeplClientError(f"Request failed: {str(e)}") from e
    except (KeyError, IndexError, ValueError) as e:
        logging.error("Failed to parse DeepL API response")
        raise DeeplClientError(f"Failed to parse API response: {str(e)}") from e
    finally:
        session.close()


def get_usage(auth_key: str, timeout: int = 10) -> Tuple[int, int]:
    """
    Get DeepL API usage statistics.

    Args:
        auth_key: DeepL API authentication key
        timeout: Request timeout in seconds (default: 10)

    Returns:
        Tuple of (character_count, character_limit)

    Raises:
        DeeplClientError: If the API request fails or returns invalid data
    """
    url = "https://api.deepl.com/v2/usage"

    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )

    # Create session with retry adapter
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)

    # Prepare headers
    headers = {"User-Agent": "linguafrancatto/2.1"}

    # Use POST with form data to avoid exposing auth_key in URL
    data = {"auth_key": auth_key}

    try:
        # Make POST request
        response = session.post(url, data=data, headers=headers, timeout=timeout)
        response.raise_for_status()

        # Parse JSON response
        result = response.json()

        # Extract usage data
        if "character_count" not in result or "character_limit" not in result:
            logging.error("DeepL API returned invalid usage response structure")
            raise DeeplClientError(
                "Invalid response from DeepL API: missing usage fields"
            )

        character_count = result["character_count"]
        character_limit = result["character_limit"]

        return (character_count, character_limit)

    except requests.exceptions.Timeout as e:
        logging.error("DeepL API usage request timed out")
        raise DeeplClientError(f"Request timed out: {str(e)}") from e
    except requests.exceptions.HTTPError as e:
        logging.error(f"DeepL API usage HTTP error: {e.response.status_code}")
        raise DeeplClientError(f"HTTP error: {e.response.status_code}") from e
    except requests.exceptions.RequestException as e:
        logging.error(f"DeepL API usage request failed: {type(e).__name__}")
        raise DeeplClientError(f"Request failed: {str(e)}") from e
    except (KeyError, ValueError) as e:
        logging.error("Failed to parse DeepL API usage response")
        raise DeeplClientError(f"Failed to parse API response: {str(e)}") from e
    finally:
        session.close()
