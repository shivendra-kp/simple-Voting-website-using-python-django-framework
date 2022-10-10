
from posixpath import split
from tokenize import String
from typing import List


def list_to_string(list) -> String:
    return ",".join(list)


def string_to_list(string ) -> List:
    return string.split(",")