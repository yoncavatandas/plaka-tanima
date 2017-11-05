#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ----------------------------------------------------------------------------
# -- Plaka Tanima - OpenAlpr
# ----------------------------------------------------------------------------
'''
import os
import sys

import argparse

import logging
import logging.handlers

import configparser

from openalpr import Alpr

# ----------------------------- GLOBAL PATHS ---------------------------------
CONF_PATH = "config.ini"
# ------------------------- GLOBAL PATHS END ---------------------------------


# ----------------------------- LOGGER CONFIG --------------------------------
LOGPATH = "logs"

if not os.path.exists(LOGPATH):
    os.mkdir(LOGPATH)

LOGFILE = "{}/openalpr.log".format(LOGPATH)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# create a file handler
HANDLER = logging.handlers.RotatingFileHandler(
    LOGFILE, maxBytes=100 * 1024 * 1024, backupCount=5)
HANDLER.setLevel(logging.INFO)

# create a logging format
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
HANDLER.setFormatter(FORMATTER)

# add the handlers to the logger
LOGGER.addHandler(HANDLER)
# ----------------------------- LOGGER CONFIG END ----------------------------


# ---------------------- ArgParse Defination START ---------------------------
PARSER = argparse.ArgumentParser(description="### PLAKA ANALIZI ###")
PARSER.add_argument('--image', help="<Image>", type=str)

ARG, _ = PARSER.parse_known_args()

ARGS = vars(ARG)

# if tpye parameter exists ~> Help
if ARGS['image'] is None:
    PARSER.print_help()
# ---------------------- ArgParse Defination END -----------------------------


# ----------------------------- CONFIG PARSER --------------------------------
CONFIG = configparser.ConfigParser()
CONFIG.read(CONF_PATH)
REGION = CONFIG.get('openalpr', 'region')
OPENALPR_CONF = CONFIG.get('openalpr', 'conf')
RUNTIME_DIR = CONFIG.get('openalpr', 'runtime')
# ------------------------- CONFIG PARSER END --------------------------------


# ----------------------------- PROCESS FUNC ---------------------------------
def process():

    alpr = Alpr(REGION, OPENALPR_CONF, RUNTIME_DIR)

    if not alpr.is_loaded():
        LOGGER.info("Error loading OpenALPR")
        sys.exit(1)

    # 5 cikarimda bulun
    alpr.set_top_n(5)

    results = alpr.recognize_file(ARGS['image'])

    i = 0
    for plate in results['results']:
        i += 1
        print("Plaka #%d" % i)
        print("   %12s %12s" % ("Plaka", "Dogruluk"))
        for candidate in plate['candidates']:
            prefix = "-"
            if candidate['matches_template']:
                prefix = "*"

            print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

    # Call when completely done to release memory
    alpr.unload()
# ----------------------------- PROCESS FUNC END -----------------------------


# --------------------------------- MAIN -------------------------------------
if __name__ == "__main__":
    process()
# --------------------------------- MAIN END ---------------------------------
