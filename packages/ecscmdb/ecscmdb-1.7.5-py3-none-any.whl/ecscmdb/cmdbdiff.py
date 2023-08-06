#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Fri Feb 17 12:54:13 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $
#

import sys
import logging
import logging.handlers

from datetime import datetime
from socket import gethostname
from pathlib import Path
import autologging
import pandas as pd

from autologging import logged, traced
from docopt import docopt
from jinja2 import Template

import ecspylibs
from ecspylibs.configfile import ConfigFile
from ecspylibs.reapchildren import ReapChildren
from ecspylibs.sendemail import SendEmail

import ecscmdb
from ecscmdb.initcheck import InitCheck
from ecscmdb.finddifferences import FindDifferences

global df_summary


@traced
@logged
def main() -> None:
    """
Program to analyze two spreadsheets for differences.

Some default option values listed below can be overridden within the initialization file.

Usage:
  %(pgm)s [-v] [-L LEVEL] [--LOG=DIR] [-c CONFIG] [-s SECTION] [-r REPORT] [-D] SPREADSHEET1 SPREADSHEET2
  %(pgm)s (-h | --help | -V | --version)

  Variables SPREADSHEET1 and SPREADSHEET2 are required, all other parameters are optional.

Options:
  -h, --help                          Show this help message and exit.
  -V, --version                       Show version information and exit.
  -c CONFIG, --config=CONFIG          The configuration file.
                                      Default: "%(--config)s"
  -s SECTION, --section=SECTION       The configuration file version (default
                                      defined within the configuration file).
  -r REPORT, --report=REPORT          Report directory or file.
  -v, --verbose                       Print verbose messages.
  -L LEVEL, --log=LEVEL               Print log messages at log value LEVEL.
                                      Valid levels are: TRACE, DEBUG, INFO, WARNING,
                                      ERROR, and CRITICAL.
                                      Default: "%(--log)s"
  --LOG=DIR                           Log Directory,
                                      Default: "%(--LOG)s"
  -D, --dryrun                        Only print out what would be done.
"""

    @traced
    @logged
    def get_col_widths(df: object) -> list:
        """Blah blah blah."""

        return [int(max([len(str(s)) for s in df[col].values] + [len(col)]) + 2.0) for col in df.columns]

    @traced
    @logged
    def fix_col_widths(ws: object, df: object) -> None:
        """Blah blah blah."""

        for i, width in enumerate(get_col_widths(df)):
            ws.set_column(i, i, width)

    TOD = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    DATE = datetime.now().strftime("%A, %B %e, %Y")
    TIME = datetime.now().strftime("%r")

    FQ_RUN_DIR = Path.cwd().resolve(strict=True)
    FQ_PGM_FILE = Path(__file__).resolve(strict=True)
    assert len(FQ_PGM_FILE.parts) >= 2
    PGM = Path(FQ_PGM_FILE.stem)
    FQ_BASE_DIR = FQ_PGM_FILE.parents[2]
    PKG = Path(__package__)

    ETC_DIR = Path("etc")
    REPORT_DIR = Path("report")
    LOG_DIR = Path("log")

    CONF_FILE = PGM.with_suffix(".yml")

    REPORT_NAME = Path(f"OpenManage-{PGM}.{TOD}.xlsx")
    LOG_FILE = PGM.with_suffix(".log")

    CONF_LIST = [
        FQ_RUN_DIR / ETC_DIR / PKG / CONF_FILE,
        FQ_RUN_DIR / ETC_DIR / CONF_FILE,
        FQ_RUN_DIR / CONF_FILE,
        FQ_BASE_DIR / ETC_DIR / PKG / CONF_FILE,
        FQ_BASE_DIR / ETC_DIR / CONF_FILE,
        FQ_BASE_DIR / CONF_FILE
    ]

    FQ_CONF_FILE = ConfigFile(CONF_LIST)
    # for tmp in CONF_LIST:
    #     if tmp.is_file():
    #         FQ_CONF_FILE = tmp.resolve(strict=True)
    #         break
    # else:
    #     print(f"Couldn't find Configuration File '{CONF_FILE.name}'.")
    #     sys.exit(1)

    FQ_REPORT_DIR = (FQ_RUN_DIR / REPORT_DIR).resolve(strict=False)
    FQ_REPORT_FILE = (FQ_REPORT_DIR / REPORT_NAME).resolve(strict=False)

    FQ_LOG_DIR = (FQ_RUN_DIR / LOG_DIR).resolve(strict=False)
    FQ_LOG_FILE = (FQ_LOG_DIR / LOG_FILE).resolve(strict=False)

    # Get hostname.

    HOST = gethostname()

    help_arguments = {
        "pgm": PGM,
        "--config": FQ_CONF_FILE.file,
        "--LOG": FQ_LOG_FILE,
        "--log": "WARNING",
        "--report": FQ_REPORT_FILE,
    }

    help_text = main.__doc__ % help_arguments

    pgm_version = f"{PGM}: {__package__}({ecscmdb.__version__}), ecspylibs({ecspylibs.__version__})"

    arguments = docopt(help_text, version=pgm_version)

    CONFIG = InitCheck(arguments, help_arguments, config="--config", section="--section")

    arguments = CONFIG.arguments
    data = CONFIG.data

    dry_run = arguments["--dryrun"]
    log_level = arguments["--log"].upper()
    log_fd = arguments["--LOG"]
    report = arguments["--report"]
    verbose = arguments["--verbose"]
    version = arguments["--version"]

    report_file = CONFIG.report_file
    log_file = CONFIG.log_file

    # Setup logging.

    log_levels = {
        "CRITICAL": logging.CRITICAL,
        "DEBUG": logging.DEBUG,
        "ERROR": logging.ERROR,
        "INFO": logging.INFO,
        "TRACE": autologging.TRACE,
        "WARNING": logging.WARNING,
    }

    logger = logging.getLogger()
    logger.setLevel(log_levels[log_level])
    log_file = log_fd

    fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=(50 * 1024 ** 2), backupCount=5)

    log_fmt = ""
    log_fmt += "%(asctime)s"
    log_fmt += " %(levelname)-7s"
    log_fmt += " [%(process)5d]"
    log_fmt += " %(module)s.py(%(funcName)s,%(lineno)d):"
    log_fmt += "\t%(message)s"

    formatter = logging.Formatter(log_fmt)

    fh.setFormatter(formatter)

    logger.addHandler(fh)

    logger.info(f"Starting program {pgm_version}.")
    if arguments["--verbose"]:
        print(f"Starting program {pgm_version}.", file=sys.stdout)

    if dry_run:
        print(f"\nList of command line arguments.\n", file=sys.stdout)

    for key in sorted(arguments.keys()):
        logger.debug(f"arguments['{key}']\t= '{arguments[key]}'")
        if dry_run:
            print(f"arguments['{key}']\t= '{arguments[key]}'", file=sys.stdout)

    del key

    my_locals = locals()
    my_locals_keys = my_locals.keys()
    my_locals_vals = my_locals.values()
    del my_locals

    if dry_run:
        print(f"\nList of all variables.\n", file=sys.stdout)

    for k, v in zip(my_locals_keys, my_locals_vals):
        logger.debug(f"{k:20} = '{v}'")
        if dry_run:
            print(f"{k:20} = '{v}'", file=sys.stdout)

    if dry_run:
        print("", file=sys.stdout)
        sys.exit(0)

    email_from = CONFIG.email_from
    email_to = CONFIG.email_to
    email_cc = CONFIG.email_cc
    subject = CONFIG.email_subject
    email_text_with_changes = CONFIG.email_text_with_changes
    email_text_without_changes = CONFIG.email_text_without_changes
    email_text_with_changes = CONFIG.email_text_with_changes
    email_text_without_changes = CONFIG.email_text_without_changes

    admin_name = CONFIG.admin_name
    admin_email = CONFIG.admin_email
    admin_phone = CONFIG.admin_phone

    spread_sheet1 = Path(arguments["SPREADSHEET1"]).resolve(strict=False)
    spread_sheet2 = Path(arguments["SPREADSHEET2"]).resolve(strict=False)

    try:
        spread_sheet1 = spread_sheet1.resolve(strict=True)
    except FileNotFoundError as e:
        logger.error(f"SPREADSHEET1 is missing or invalid: '{spread_sheet1}'")
        print(f"\nError: SPREADSHEET1 is missing or invalid: '{spread_sheet1}'\n", file=sys.stderr)
    except Exception as e:
        logger.error(f"\nException: {e=}")
        print(f"\nException: {e=}\n", file=sys.stderr)
        sys.exit(1)

    try:
        spread_sheet2 = spread_sheet2.resolve(strict=True)
    except FileNotFoundError as e:
        logger.error(f"SPREADSHEET2 is missing or invalid: '{spread_sheet2}'")
        print(f"\nError: SPREADSHEET2 is missing or invalid: '{spread_sheet2}'\n", file=sys.stderr)
    except Exception as e:
        print(f"\nException: {e=}\n", file=sys.stderr)
        sys.exit(1)

    short_spread_sheet1 = spread_sheet1.name
    short_spread_sheet2 = spread_sheet2.name

    if dry_run:
        print(f"\nList of command line arguments.\n", file=sys.stdout)

    for key in sorted(arguments.keys()):
        logger.debug(f"arguments['{key}']\t= '{arguments[key]}'")
        if dry_run:
            print(f"arguments['{key}']\t= '{arguments[key]}'", file=sys.stdout)

    del key

    my_locals = locals()
    my_locals_keys = my_locals.keys()
    my_locals_vals = my_locals.values()
    del my_locals

    if dry_run:
        print(f"\nList of all variables.\n", file=sys.stdout)

    for k, v in zip(my_locals_keys, my_locals_vals):
        logger.debug(f"{k:20} = '{v}'")
        if dry_run:
            print(f"{k:20} = '{v}'", file=sys.stdout)

    if dry_run:
        print("", file=sys.stdout)
        sys.exit(0)

    # The real stuff goes here.

    excel = pd.ExcelWriter(report)

    logger.debug(f"Create df_spread_sheet1 from file '{spread_sheet1}'.")
    try:
        df_spread_sheet1 = pd.read_excel(spread_sheet1, sheet_name=None)
    except Exception as e:
        logger.critical(f"Failed to read '{spread_sheet1}' Spreadsheet.")
        logger.exception(f"Exception: '{e}'.")
        logger.info(f"Ending program {pgm_version}.")
        if verbose:
            print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
        sys.exit(1)

    logger.debug(f"Create df_spread_sheet2 from file '{spread_sheet2}'.")
    try:
        df_spread_sheet2 = pd.read_excel(spread_sheet2, sheet_name=None)
    except Exception as e:
        logger.critical(f"Failed to read '{spread_sheet2}' spreadsheet.")
        logger.exception(f"Exception: '{e}'.")
        logger.info(f"Ending program {pgm_version}..")
        if verbose:
            print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
        sys.exit(1)

    sheet_names1 = set(df_spread_sheet1.keys())
    logger.debug(f"sheet_names1: '{sheet_names1}'")
    worksheets1 = len(sheet_names1)
    logger.debug(f"worksheets1: '{worksheets1}'")

    sheet_names2 = set(df_spread_sheet2.keys())
    logger.debug(f"sheet_names2: '{sheet_names2}'")
    worksheets2 = len(sheet_names2)
    logger.debug(f"worksheets2: '{worksheets2}'")

    deleted_sheet_names1 = sheet_names1.difference(sheet_names2)
    logger.debug(f"deleted_sheet_names1: '{deleted_sheet_names1}'")

    deleted_sheet_names2 = sheet_names2.difference(sheet_names1)
    logger.debug(f"deleted_sheet_names2: '{deleted_sheet_names2}'")

    common_sheet_names = list(sheet_names1.intersection(sheet_names2))
    common_sheet_names.sort()
    logger.debug(f"common_sheet_names: '{common_sheet_names}'")

    if verbose:
        print(f"\n=====================================================\n", file=sys.stdout)
        print(f"Analyzing spreadsheet:\n\t '{short_spread_sheet1}'\n", file=sys.stdout)
        print(f"with spreadsheet:\n\t '{short_spread_sheet2}'", file=sys.stdout)
        print(f"\n=====================================================\n", file=sys.stdout)

    logger.info(f"Creating the Summary sheet.")

    details_column = f"See sheet tab for details."
    df_summary = pd.DataFrame()
    df_summary["Summary of changes."] = ""
    df_summary["See sheet tab for details."] = ""

    cols = df_summary.columns.tolist()
    cols.insert(0, cols.pop(cols.index("Summary of changes.")))

    df_summary = df_summary.reindex(columns=cols)
    df_summary.to_excel(excel, "Summary", index=False)

    df_summary = df_summary.append(
        {
            "Summary of changes.": f"Comparing '{short_spread_sheet1}' with '{short_spread_sheet2}' on {DATE} {TIME}.",
        }, ignore_index=True)

    df_summary = df_summary.append(
        {
            "Summary of changes.": f"All changes listed in this Summary page are relative to '{short_spread_sheet2}'.",
        }, ignore_index=True)

    df_summary = df_summary.append(
        {
            "Summary of changes.": f"",
        }, ignore_index=True)

    data_changes = False

    if verbose:
        print(f"Looking for added or deleted sheet names in spreadsheets:", end="", file=sys.stdout)

    if deleted_sheet_names1 or deleted_sheet_names2:
        data_changes = True

        if verbose:
            print(f"\n\nThe following sheet name(s) changed in the spreadsheet:\n", file=sys.stdout)

        if deleted_sheet_names2:
            if verbose:
                print(f"Sheet name(s) added:", file=sys.stdout)

            for added in deleted_sheet_names2:
                if verbose:
                    print(f"\t{added}", file=sys.stdout)

                df_summary = df_summary.append(
                    {
                        "Summary of changes.": f"Sheet '{added}' added.",
                        "See sheet tab for details.": f"{added}",
                    }, ignore_index=True)

                df_sheet = pd.DataFrame(df_spread_sheet2[added])
                df_sheet.to_excel(excel, added, index=False)
                fix_col_widths(excel.sheets[added], df_sheet)

        if deleted_sheet_names1 and deleted_sheet_names2:
            if verbose:
                print(f"", file=sys.stdout)

        if deleted_sheet_names1:
            if verbose:
                print(f"Sheet name(s) deleted:", file=sys.stdout)

            for deleted in deleted_sheet_names1:
                if verbose:
                    print(f"\t{deleted}", file=sys.stdout)

                df_summary = df_summary.append(
                    {
                        "Summary of changes.": f"Sheet '{deleted}' deleted.",
                        "See sheet tab for details.": f"{deleted}",
                    }, ignore_index=True)

                df_sheet = pd.DataFrame(df_spread_sheet1[deleted])
                df_sheet.to_excel(excel, deleted, index=False)
                fix_col_widths(excel.sheets[deleted], df_sheet)

        if verbose:
            print(f"\nThe sheet name(s) listed above will be ignored when analyzing the spreadsheets.\n",
                  file=sys.stdout)

    else:
        logger.info(f"There were no sheets added or deleted in either of the CMDB spreadsheets.")
        if verbose:
            print(f" None", file=sys.stdout)

        df_summary = df_summary.append(
            {
                "Summary of changes.": f"There were no sheets added or deleted in either of the CMDB spreadsheets.",
                "See sheet tab for details.": f"None",
            }, ignore_index=True)

    data_changes = False

    print(f"Looking for sheets with data changes.", file=sys.stdout)

    find_diffs = FindDifferences(df_spread_sheet1, df_spread_sheet2, df_summary)

    for sheet in common_sheet_names:
        df_spread_sheet1[sheet] = df_spread_sheet1[sheet].fillna("")
        df_spread_sheet2[sheet] = df_spread_sheet2[sheet].fillna("")

        if not df_spread_sheet2[sheet].equals(df_spread_sheet1[sheet]):
            logger.info(f"Sheet '{sheet}' has changes.")
            print(f"Sheet '{sheet}' has changes.", file=sys.stdout)

            df_style, df_sheet, df_summary = find_diffs.find_differences(sheet)
            df_style = df_sheet.style.apply(find_diffs.set_style, style=df_style, axis=None)

            data_changes = True

            df_style.to_excel(excel, sheet, index=False)
            fix_col_widths(excel.sheets[sheet], df_sheet)

        else:
            logger.info(f"Sheet '{sheet}' has no changes.")

    if not data_changes:
        logger.info(f"There was no data changes in any sheet in either of the CMDB spreadsheets.")
        if verbose:
            print(f"There was no data changes in any sheet in either of the CMDB spreadsheets.", file=sys.stdout)

        df_summary = df_summary.append(
            {
                "Summary of changes.": f"There was no data changes in any sheet in either of the CMDB spreadsheets.",
                "See sheet tab for details.": f"None",
            }, ignore_index=True)

        print(f"\n=====================================================\n", file=sys.stdout)

    logger.info(f"Update the Summary sheet.")
    df_summary.to_excel(excel, "Summary", index=False)

    logger.info(f"Fix Column Widths for the Summary sheet.")
    fix_col_widths(excel.sheets["Summary"], df_summary)

    logger.info(f"Write out the Report spreadsheet.")
    excel.save()
    excel.close()

    logger.info(f"Create report.")

    # Fix all jinja2 strings.

    replacement = {
        "ADMINEMAIL": admin_email,
        "ADMINNAME": admin_name,
        "ADMINPHONE": admin_phone,
        "DATE": DATE,
        "HOST": HOST,
        "REPORT": report_file.name,
        "SPREADSHEET1": short_spread_sheet1,
        "SPREADSHEET2": short_spread_sheet2,
        "TIME": TIME,
        "VERSION": pgm_version,
        "WORKSHEETS1": worksheets1,
        "WORKSHEETS2": worksheets2,
    }

    if data_changes:
        logger.info(f"Using text for when data changed between spreadsheets.")
        text = email_text_with_changes
    else:
        logger.info(f"Using text for when data did not change between spreadsheets.")
        text = email_text_without_changes

    logger.debug(f"text(1) : {text}")

    logger.info(f"Updating variables email_from, subject, and text.")
    email_from = Template(email_from).render(replacement)
    subject = Template(subject).render(replacement)
    text = Template(text).render(replacement)

    logger.debug(f"email_from : '{email_from}'.")
    logger.debug(f"email_to : '{email_to}'.")
    logger.debug(f"email_cc : '{email_cc}'.")
    logger.debug(f"subject : '{subject}'.")
    logger.debug(f"text(2) : '{text}'")

    sm = SendEmail()
    sm.send_email(email_from, email_to, email_cc, subject, text, text_type="plain",
                  files=[spread_sheet1, spread_sheet2, report], server="localhost")

    rc = ReapChildren()
    try:
        rc.reap_children()
    except Exception as e:
        logger.critical(f"Fatal error occurred in reapChildren().")
        logger.exception(f"Exception: '{e}'.")

    logger.info(f"Ending program {pgm_version}.")
    if verbose:
        print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
