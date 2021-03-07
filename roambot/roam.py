import os
import subprocess
import json
import operator


# TODO: If this ever gets more complicated than this, consider turning it into a class
def block_search(tag, roam_api_graph, roam_api_email, roam_api_password, max_length=None):
    """Search roam graph for blocks with a particular tag.

    Note:
        Requires the `roam-api` javascript node module to be installed.

    Args:
        tag: The roam backlink to search for.
        roam_api_graph: The name of your Roam graph
        roam_api_email: The email used to register for Roam Research
        roam_api_password: The password for your Roam Research account
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
    env = {}
    env.update(os.environ)
    env.update({
        "ROAM_API_GRAPH": roam_api_graph,
        "ROAM_API_EMAIL": roam_api_email,
        "ROAM_API_PASSWORD": roam_api_password,
    })
    out = subprocess.check_output(
        ["roam-api", "query", f"'{query}'"],
        stderr=subprocess.STDOUT,
        env=env
    )
    # TODO: contribute silent mode for CLI
    json_str = "\n".join(out.decode().split("\n")[2:])  # strip cli info output
    data = list(map(operator.itemgetter(1), json.loads(json_str)))

    if max_length is not None:
        data = [d for d in data if len(data) < max_length]

    return data
