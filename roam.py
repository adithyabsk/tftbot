import subprocess
import json
import operator


def block_search(tag, max_length=None):
    """Search roam database for blocks with a particular tag.

    Args:
        tag: The roam backlink to search for.
        max_length: The max length of a tag

    Return:
        A list of found blocks.

    """
    # source: https://davidbieber.com/snippets/2021-01-04-more-datalog-queries-for-roam/
    # TODO: I need to understand dataomic better so I can expand this to arbitrary length tags
    # TODO: arbitrary boolean logic for including and excluding tags
    # TODO: rules for snagging tag children.
    query = f"""[
        :find ?uid ?string
        :where
        [?block :block/uid ?uid]
        [?block :block/string ?string]
        [?block :block/refs ?block_tag1]
        [?block_tag1 :node/title "{tag}"]
    ]"""
    query = " ".join(query.split())
    out = subprocess.check_output(["roam-api", "query", f"'{query}'"])
    # TODO: contribute silent mode for CLI
    json_str = "\n".join(out.decode().split("\n")[2:])  # strip cli info output
    data = list(map(operator.itemgetter(1), json.loads(json_str)))

    if max_length is not None:
        data = [d for d in data if len(data) < max_length]

    return data


if __name__ == "__main__":
    block_search("idea")
