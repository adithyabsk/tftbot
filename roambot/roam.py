import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

ROAM_SIGNIN_URL = "https://roamresearch.com/#/signin"
ROAM_APP_URL = "https://roamresearch.com/#/app"
TIMEOUT = 15


def setup_roam_browser(roam_api_graph, roam_api_email, roam_api_password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    browser = webdriver.Chrome(options=chrome_options, service_log_path=os.devnull)

    browser.get(ROAM_SIGNIN_URL)
    wait = WebDriverWait(browser, TIMEOUT)

    # Check that we are on the sign in page
    time.sleep(2)
    wait.until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "input[name='email']")),
        "failed to navigate to sign in page"
    )

    # Fill Email and Password and log in
    email_elem = browser.find_element_by_css_selector("input[name='email']")
    email_elem.send_keys(roam_api_email)
    passwd_elem = browser.find_element_by_css_selector("input[name='password']")
    passwd_elem.send_keys(roam_api_password)
    passwd_elem.send_keys(Keys.RETURN)

    # Check that we are on the graph list page
    wait.until(expected_conditions.url_to_be(ROAM_APP_URL), "failed to navigate to graph list page")
    graph_url = ROAM_APP_URL+f"/{roam_api_graph}"
    browser.get(graph_url)

    # Check that we are now on the graph page
    wait.until(expected_conditions.url_to_be(graph_url), "failed to navigate to graph page")

    # The page is fully loaded
    wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "roam-main")),
               "failed to navigate to graph page")

    return browser


def run_query(browser, query):
    norm_query = " ".join(query.split())
    check_element = "return window.roamAlphaAPI"

    if not browser.execute_script(check_element):
        raise ValueError("RoamAPI not found")

    # Run query using roam js API in browser
    get_query = f"return window.roamAlphaAPI.q('{norm_query}')"
    # Get the string pair data of the form [["id", "note"], ...]
    data_pairs = browser.execute_script(get_query)

    return data_pairs


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
    # TODO: I need to understand datalog better so I can expand this to arbitrary length tags
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
    browser = setup_roam_browser(roam_api_graph, roam_api_email, roam_api_password)
    data_pairs = run_query(browser, query)

    # data = list(map(operator.itemgetter(1), data_pairs))

    # Check to make sure that the strings are smaller than `max_length`
    if max_length is not None:
        data_pairs = [d for d in data_pairs if len(d[1]) < max_length]

    return data_pairs
