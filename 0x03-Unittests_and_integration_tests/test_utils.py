#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from parameterized import parameterized
from utils import access_nested_map  # Make sure utils.py exists in the same folder

class TestAccessNestedMap(unittest.TestCase):
    """Test case for access_nested_map"""

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        """Test that KeyError is raised with correct message"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_message}'")
