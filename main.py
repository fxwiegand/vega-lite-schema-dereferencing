import json
from resolve import resolve_json, remove_recursive_definitions
import httpx


if __name__ == '__main__':
    response = httpx.get("https://vega.github.io/schema/vega-lite/v5.json")
    schema_with_references = response.json()

    with open("original.json", "w") as outfile:
        json.dump(schema_with_references, outfile, indent=4)
        schema_with_references_no_recursion = remove_recursive_definitions(schema_with_references)
        resolved = resolve_json(schema_with_references_no_recursion)

    with open("resolved.json", "w") as outfile:
        json.dump(resolved, outfile, indent=4)
