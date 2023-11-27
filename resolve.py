import copy

from dollar_ref import pluck


def test_deref():
    example = {
        'some': 'thing',
        'sub-document': {
            'we-do-not': 'need-this',
            'go-deeper': 'than-this',
            'need-recursion': {
                'more-awesome': 'data',
                'we': {
                    'could': {
                        'need': {
                            '$ref': '#/sub-document/need-recursion',
                        }
                    }
                }
            },
            'target': {
                'awesome': 'data',
                'we': [
                    {
                        '$ref': '#/sub-document/we-do-not'
                    },
                    {
                        'might': {
                            'use': {
                                '$ref': '#/sub-document/go-deeper',
                            }
                        }
                    }
                ]
            }
        }
    }

    no_recursion = remove_recursive_definitions(example)
    print(no_recursion)
    print(resolve_json(example))


def resolve_json(json):
    def resolve_ref(obj, ref_path):
        keys = ref_path.split('/')
        for key in keys:
            if key:
                obj = obj[key]
        return obj

    def resolve_recursive(value, original_structure):
        if isinstance(value, dict):
            resolved_dict = {}
            for key, sub_value in value.items():
                if isinstance(sub_value, dict) and "$ref" in sub_value:
                    ref_path = sub_value["$ref"][2:]  # Remove '#/' prefix
                    resolved_value = resolve_ref(original_structure, ref_path)
                    resolved_dict[key] = resolve_recursive(resolved_value, original_structure)
                else:
                    resolved_dict[key] = resolve_recursive(sub_value, original_structure)
            return resolved_dict
        elif isinstance(value, list):
            resolved_list = []
            for item in value:
                if isinstance(item, dict):
                    if "$ref" in item:
                        ref_path = item["$ref"][2:]  # Remove '#/' prefix
                        resolved_item = resolve_ref(original_structure, ref_path)
                        resolved_list.append(resolve_recursive(resolved_item, original_structure))
                    else:
                        resolved_list.append(resolve_recursive(item, original_structure))
                else:
                    resolved_list.append(item)
            return resolved_list
        else:
            return value

    # Create a deep copy of the original JSON to avoid modifying it
    resolved_json = copy.deepcopy(json)

    # Resolve references recursively
    resolved_json = resolve_recursive(resolved_json, json)

    return resolved_json


def remove_recursive_definitions(schema):
    def process_node(node, visited_paths):
        if isinstance(node, dict):
            if "$ref" in node:
                ref_path = node["$ref"]
                if ref_path not in visited_paths:
                    visited_paths.add(ref_path)
                    process_node(get_nested_value(schema, ref_path), visited_paths)
                else:
                    # Remove recursive definition
                    del node["$ref"]
            else:
                for key, value in node.items():
                    process_node(value, visited_paths)
        elif isinstance(node, list):
            for item in node:
                process_node(item, visited_paths)

    def get_nested_value(obj, path):
        if path.startswith('#/'):
            path = path[2:]  # Remove '#' prefix
        keys = path.split('/')
        for key in keys:
            if key:
                obj = obj[key]
        return obj

    process_node(schema, set())
    return schema
