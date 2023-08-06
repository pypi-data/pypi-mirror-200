# import private
import configparser
import os

# const
CFG_FILENAME = r"user_settings.cfg"
# CFG info
cfg = configparser.ConfigParser()

def save():
    with open(CFG_FILENAME,"w") as config_file:
        cfg.write(config_file)

def load():
    # Set deafults
    cfg["form"] = {"filter_dir": os.path.expanduser("~/Documents")+"/My Games/Path of Exile/",
                   "filter_name":"Browse To Select",
                   "username":"",
                   "league":"",
                   "tab":""}
    cfg["api"] = {"CLIENT_ID":"chipytools",
                  "CLIENT_SECRET":"AskChipyForThis",
                  "SCOPE":"account:profile account:characters account:stashes account:item_filter",
                  "REDIRECT_URI":"https://chipy.dev/poe_auth.html",
                  "TOKEN":"",
                  }
    cfg.read(CFG_FILENAME)

def get(section:str, key:str) -> str:
    return cfg.get(section, key,fallback="MISSING")

def set(section:str, key:str, value:str):
    cfg[section][key] = value
    save()

# load base info
load()

if __name__ == "__main__":
    print(get("api","client_id"))
    load()
    print(get("api","client_id"))
    save()