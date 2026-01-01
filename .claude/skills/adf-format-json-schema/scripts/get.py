# -*- coding: utf-8 -*-

import json

import fire

from atlas_doc_parser.tests.data.schema import adf_json_schema


class Command:
    def list_def(self):
        defs = list(adf_json_schema.data["definitions"])
        defs.sort()
        for def_name in defs:
            def_value = adf_json_schema.data["definitions"][def_name]
            properties = list(def_value.get("properties", {}))
            print(f"name = {def_name}, properties = {properties}")

    def get_def(self, def_name: str):
        def_value = adf_json_schema.data["definitions"][def_name]
        print(json.dumps(def_value, indent=2))


if __name__ == "__main__":
    fire.Fire(Command)
