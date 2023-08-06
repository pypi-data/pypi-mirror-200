import os
import sys
import json


HOME = os.environ["HOME"]
XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", f"{HOME}/.config")
BARE_ESTATE_LOCATION = os.environ.get("BARE_ESTATE_LOCATION", None)
CONFIG_FILE = "bare_estate.json"


try:
    if BARE_ESTATE_LOCATION is None:
        with open(f"{XDG_CONFIG_HOME}/{CONFIG_FILE}") as config_file:
            configs = json.load(config_file)
    else:
        configs = { "history_location": BARE_ESTATE_LOCATION }

except FileNotFoundError:
    config_file = f"{XDG_CONFIG_HOME}/{CONFIG_FILE}"
    print("Error: the configuration file %s was not found" %config_file,
          file=sys.stderr)
    sys.exit(1)
