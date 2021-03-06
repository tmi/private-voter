from configparser import ConfigParser
import logging
import os
import sys
import io
import pkg_resources

configs = ConfigParser()

def initDefault():
    with pkg_resources.resource_stream("privateVoterFront.config", "default.ini") as defaultConfigStream:
        configs.read_file(io.TextIOWrapper(defaultConfigStream))
    valueOption = os.environ.get("INI_FILE")
    if (valueOption):
        fname = valueOption.strip()
        if not os.path.exists(fname):
            raise FileNotFoundError(f"not found config file {fname}")
        configs.read(fname)

def initLogging():
    target = configs.get("LOGGING", "TARGET")
    numeric_level = getattr(logging, configs.get("LOGGING", "LEVEL").upper())

    root = logging.getLogger()
    root.setLevel(numeric_level)

    if (target == "stdout"):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(numeric_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

def get(section, value):
    return configs.get(section, value)
