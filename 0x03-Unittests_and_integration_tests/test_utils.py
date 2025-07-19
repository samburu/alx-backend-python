#!/usr/bin/env python3
"""
Unit tests for access_nested_map.
"""

import unittest
from parameterized import parameterized
from .utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """Test access_nested_map raises KeyError with expected message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(expected))


if __name__ == '__main__':
    unittest.main()
