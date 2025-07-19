#!/usr/bin/env python3
"""
Unit tests for access_nested_map.
"""

import unittest
from unittest.mock import Mock, patch

from parameterized import parameterized

from .utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for the access_nested_map function.
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",), "a"),
            ({"a": 1}, ("a", "b"), "b"),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test access_nested_map raises KeyError with expected message"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test get_json returns expected payload and calls requests.get properly
        """

        # Mock the response object's json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        # Assert requests.get called once with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert get_json returns the mocked payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoization caches method results."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as m_method:
            instance = TestClass()

            # First call should call the method
            result1 = instance.a_property

            # Second call should return cached value
            result2 = instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # a_method should only be called once due to memoization
            m_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
