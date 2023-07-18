# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Felix Nützel

from weaviate.embedded import EmbeddedOptions
import weaviate
from prettytable import PrettyTable
import sys
import os
import re
import textwrap

LIMIT = 1000
MAX_TEXT_LENGTH = 150


def print_index_content(index_name=None, condition=None, limit=LIMIT):
    """
    A function to print index content as tables or to print all indeces with their properties.
    :param index_name: Name of the class you want to see. Leave as None if you want to see the classes and their properties
    :param limit: Limit the number of entries you want to see.
    :param condition: a string of the form '<property_index><operator><value>'
    """

    # silences log messages from startup
    fd = os.open("/dev/null", os.O_WRONLY)
    os.dup2(fd, 2)

    weaviate_client = weaviate.Client(embedded_options=EmbeddedOptions())
    index_dict = weaviate_client.schema.get(index_name)
    if index_name is None:
        for class_info in index_dict["classes"]:
            print(f"Class: {class_info['class']}")
            print("Properties:")
            for property in class_info["properties"]:
                print(f"\tProperty name: {property['name']}")
                print(f"\tData type: {property['dataType']}")
                if "description" in property:
                    print(f"\tDescription: {property['description']}")
                print("\n")
    else:
        properties = []
        for property in index_dict["properties"]:
            properties.append(property["name"])
        if condition is None:
            result = (
                weaviate_client.query.get(index_name, properties).with_limit(limit).do()
            )
        else:
            pattern = r"^(\d+)(And|Or|Equal|NotEqual|GreaterThan|GreaterThanEqual|LessThan|LessThanEqual|Like)(\S+)$"
            match = re.match(pattern, condition)
            if match:
                condition_tuple = match.groups()
                result = (
                    weaviate_client.query.get(index_name, properties)
                    .with_where(
                        {
                            "path": [properties[int(condition_tuple[0])]],
                            "operator": condition_tuple[1],
                            "valueString": condition_tuple[2],
                        }
                    )
                    .with_limit(limit)
                    .do()
                )
            else:
                sys.exit("Bad condition format!")

        table = PrettyTable()
        table.field_names = properties
        for record in result["data"]["Get"][index_name]:
            row = [record[property] for property in properties]
            table.add_row([*row[:-1], wrap_text(row[-1], MAX_TEXT_LENGTH)])
        table.align = "l"
        print(table)


def wrap_text(text, max_width):
    return "\n".join(textwrap.wrap(text, max_width))


if __name__ == "__main__":
    print_index_content(*sys.argv[1:])
