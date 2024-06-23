from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import json
import requests
import time
import re
import base64


def process_browser_logs_for_network_events(logs):
    """
    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
    since we're interested in the network events specifically.
    """
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
            "Network.response" in log["method"]
            or "Network.request" in log["method"]
            or "Network.webSocket" in log["method"]
        ):
            yield log


def getSeleniumToken(url):

    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

    # Configure Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the Chrome webdriver with configured options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)

    logs = driver.get_log("performance")

    events = process_browser_logs_for_network_events(logs)

    client_token = None
    authorization = None
    persisted_query = None

    for event in events:

        try:

            if client_token and authorization and persisted_query:
                break
            if (
                event["params"]["request"]["headers"]["client-token"]
                and client_token is None
            ):
                client_token = event["params"]["request"]["headers"]["client-token"]
                authorization = event["params"]["request"]["headers"]["authorization"]
            if (
                "https://api-partner.spotify.com/pathfinder/v1/query"
                in event["params"]["request"]["url"]
                and persisted_query is None
            ):
                persisted_query = event["params"]["request"]["url"].split(
                    "extensions="
                )[1]
        except Exception as e:
            pass

    # Close the webdriver
    driver.quit()

    return authorization, persisted_query


def getToken(url):
    ua = UserAgent()
    header = {"User-Agent": str(ua.random)}
    response = requests.get(url, headers=header)

    if response.status_code == 200:
        html = response.text
        access_token_match = re.search(r'accessToken":"(.*?)"', html)
        if access_token_match:
            access_token = access_token_match.group(1)
            return {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
    else:
        return None


def getAuthToken():

    if not refreshToken():
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {read_config()[2]}",
        }
    return None


def refreshToken():
    client_id = "6dba0e90f6744a0398dedd802a56d270"
    client_secret = "21f51bd8f0a24708948068e3472b6bdb"

    o, r, a, x = read_config()

    if o:
        if x > datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
            return False
        auth_options = {
            "url": "https://accounts.spotify.com/api/token",
            "data": {
                "grant_type": "refresh_token",
                "refresh_token": r,
                "client_id": client_id,
            },
            "headers": {
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": "Basic "
                + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
            },
        }
        response = requests.post(**auth_options)

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            print("Refreshed Access Token")
            with open("spotify_auth.json", "w") as file:
                current_time = datetime.now()
                new_time = current_time + timedelta(
                    seconds=int(response.json().get("expires_in", "0"))
                )
                w_data = {
                    "authenticated": True,
                    "refresh_token": response.json().get("refresh_token", r),
                    "access_token": access_token,
                    "expiry": new_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                file.write(json.dumps(w_data, indent=4))
            return True


def read_config():
    with open("spotify_auth.json", "r") as file:
        config = json.load(file)
    return (
        config.get("authenticated", False),
        config.get("refresh_token", ""),
        config.get("access_token", ""),
        config.get("expiry", ""),
    )


if __name__ == "__main__":

    # url = "https://open.spotify.com/user/314dchp5nqd2ic4nuadhkw5prqwq/following"

    # getToken(url)
    print(
        getSeleniumToken(
            "https://open.spotify.com/artist/3b2q69EvD3tLQDKiYSd5uo/discovered-on"
        )
    )
