import unittest
from resolve import remove_recursive_definitions, resolve_json


class TestJsonResolver(unittest.TestCase):
    def test_remove_recursive_definitions(self):
        schema = {
            'a': {
                'b': {
                    '$ref': '#/a',
                }
            }
        }

        expected_result = {'a': {'b': {}}}
        result = remove_recursive_definitions(schema)
        self.assertEqual(result, expected_result)

    def test_resolve_json(self):
        json_with_reference = {
            'a': {
                'b': 'data',
                'c': {
                    '$ref': '#/a/b',
                }
            }
        }

        expected_result = {
            'a': {
                'b': 'data',
                'c': 'data',
            }
        }

        result = resolve_json(json_with_reference)
        self.assertEqual(result, expected_result)

    def test_resolve_json_with_array(self):
        json_with_reference = {
            'a': {
                'b': 'data',
                'c': {
                    '$ref': '#/a/b',
                },
                'f': 'foo'
            },
            'd': [
                {
                    'e': {
                        '$ref': '#/a/f',
                    }
                }
            ]
        }

        expected_result = {
            'a': {
                'b': 'data',
                'c': 'data',
                'f': 'foo'
            },
            'd': [
                {
                    'e': 'foo'
                }
            ]
        }

        result = resolve_json(json_with_reference)
        self.assertEqual(result, expected_result)