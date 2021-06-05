from splinter import Browser
from getpass import getpass
from plumbum import FG
from plumbum.cmd import sudo, openconnect

DOMAIN = dict(
    staff="staff.main.ntu.edu.sg",
)


def connect_cmd(dsid):
    cmd = openconnect[
        "https://ntuvpn.ntu.edu.sg/saml",
        "--protocol", "nc",
        "--cookie", f"DSID={dsid}",
    ]
    sudo[cmd] & FG


def connect_as_staff(username, password):
    browser = Browser()
    browser.visit("https://ntuvpn.ntu.edu.sg/saml")
    browser.fill("UserName", username)
    browser.fill("Password", password)
    browser.find_by_id("submitButton").click()
    if not browser.is_text_present("You have logged into NTU VPN", wait_time=300):
        raise Exception("Log in failed!")
    dsid = browser.cookies["DSID"]
    browser.quit()
    connect_cmd(dsid)


if __name__ == '__main__':
    username = input("Username:")
    domain = input("Domain[staff]:") or "staff"
    if domain != "staff":
        print("Only staff is tested for now.")
        exit()
    if "ntu.edu.sg" not in username:
        username = f"{username}@{DOMAIN[domain]}"
    password = getpass()
    connect_as_staff(username, password)
