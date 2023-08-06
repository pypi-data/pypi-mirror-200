import json
from typing import List, Dict, Union

from httpie.cli.argtypes import KeyValueArgType
from httpie.cli.constants import *
from httpie.cli.nested_json import interpret_nested_json

JSONType = Union[str, bool, int, list, dict]
KV_PAIR_SEPARATOR = ","
JSON_FILE_PARAM_TYPE = "JSON_FILE"
JSON_LITERAL_PARAM_TYPE = "JSON_LITERAL"
KV_PARAM_TYPE = "KEY_VALUE"
UNKNOWN_PARAM_TYPE = "UNKNOWN"


def merge(base, override_dict, path=None):
    """
    merges b into a
    """
    if path is None:
        path = []
    for key in override_dict:
        if key in base:
            if isinstance(base[key], dict) and isinstance(override_dict[key], dict):
                merge(base[key], override_dict[key], path + [str(key)])
            elif base[key] == override_dict[key]:
                pass  # same leaf value
            else:
                # o
                base[key] = override_dict[key]
        else:
            base[key] = override_dict[key]
    return base


def split_kv_pairs(kv_pairs: str) -> List[str]:
    kv_pairs = kv_pairs.replace("\\,", "%2C")
    return [kv_pair.replace("\\,", ",").replace("%2C", ",") for kv_pair in kv_pairs.split(KV_PAIR_SEPARATOR)]


def is_json_object_or_array_string(string: str) -> bool:
    try:
        json_val = json.loads(string)
        return isinstance(json_val, list) or isinstance(json_val, dict)
    except ValueError as e:
        return False


def get_argument_type(argument: str) -> str:
    if not argument:
        return UNKNOWN_PARAM_TYPE
    if argument.startswith("@"):
        return JSON_FILE_PARAM_TYPE
    if is_json_object_or_array_string(argument):
        return JSON_LITERAL_PARAM_TYPE
    return KV_PARAM_TYPE


def parse_kv_arguments(arguments: List[str]) -> Dict[str, JSONType]:
    arg_types = KeyValueArgType(*SEPARATOR_GROUP_NESTED_JSON_ITEMS)
    kv_pairs = list()
    for argument in arguments:
        arg_type = arg_types(argument)
        if arg_type.sep == SEPARATOR_DATA_EMBED_FILE_CONTENTS:
            with open(arg_type.value) as arg_fp:
                arg_type.value = arg_fp.read()
        elif arg_type.sep == SEPARATOR_DATA_EMBED_RAW_JSON_FILE:
            with open(arg_type.value) as arg_fp:
                arg_type.value = json.load(arg_fp)
        elif arg_type.sep == SEPARATOR_DATA_RAW_JSON:
            arg_type.value = json.loads(arg_type.value)
        kv_pairs.append((arg_type.key, arg_type.value))
    return interpret_nested_json(kv_pairs)


def parse_argument(argument: str, argument_type: str = None) -> Dict[str, JSONType]:
    if not argument:
        return {}
    if not argument_type:
        argument_type = get_argument_type(argument)
    argument = argument.strip()
    if argument_type == JSON_FILE_PARAM_TYPE:
        with open(argument.replace("@", "", 1)) as param_file:
            return json.load(param_file)
    # If the param is a valid json string, parse it and return the json object.
    elif argument_type == JSON_LITERAL_PARAM_TYPE:
        return json.loads(argument)
    elif argument_type == KV_PARAM_TYPE:
        return parse_kv_arguments(split_kv_pairs(argument))
    else:
        raise ValueError(f"Unknown input value type supplied for '{argument}'")


def parse_and_merge_arguments(arguments: List[str]) -> Dict[str, JSONType]:
    arguments_results = dict()
    kv_arguments = list()
    for argument in arguments:
        argument_type = get_argument_type(argument)
        if argument_type == KV_PARAM_TYPE:
            kv_arguments.extend(split_kv_pairs(argument))
        else:
            parsed = parse_argument(argument, argument_type)
            merge(arguments_results, parsed)
    kv_arguments_result = parse_kv_arguments(kv_arguments)
    merge(arguments_results, kv_arguments_result)
    return arguments_results
