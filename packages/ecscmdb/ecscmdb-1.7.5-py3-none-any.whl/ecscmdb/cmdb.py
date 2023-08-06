#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Wed Mar 8 10:48:34 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $
#

import logging
import logging.handlers
import sys

from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from getpass import getpass
from pathlib import Path

import autologging
import ecspylibs
import pandas as pd

from autologging import logged, traced
from docopt import docopt
from ecspylibs.configfile import ConfigFile
from ecspylibs.parallel import Parallel
from ecspylibs.password import Password
from ecspylibs.reapchildren import ReapChildren
from pandas import json_normalize

import ecscmdb
from ecscmdb.api import API
from ecscmdb.initcheck import InitCheck
from ecscmdb.updatecells import UpdateCells


@traced
@logged
def get_col_widths(df: object) -> list:
    return [int(max([len(str(s)) for s in df[col].values] + [len(col)]) + 2.0) for col in df.columns]


@traced
@logged
def set_col_widths(ws: object, df: object) -> None:
    for i, width in enumerate(get_col_widths(df)):
        ws.set_column(i, i, width)


@traced
@logged
def reformat_text(text: object, max_len: object = 100) -> str:
    """
    Doc String
    """

    text_out = ""
    for i in text.splitlines():
        line = ""
        for w in i.split(" "):
            if len(f"{line} {w}") > max_len:
                text_out += line + "\n"
                line = w
            elif len(w) == 0:
                text_out += "\n"
            elif len(line) == 0:
                line = w
            else:
                line += f" {w}"
        if len(line) > 0:
            text_out += line + "\n"
    return text_out


@traced
@logged
def main() -> None:

    """
Program to download the data from the OpenManage DB and build a spreadsheet.

Some default option values listed below can be overridden within the
configuration file.

Usage:
  %(pgm)s [-v] [-L LEVEL] [--LOG=DIR] [-f] [-F FILTER] [-c CONFIG] [-s SECTION] [-o OUTPUT] [-p PWFILE] [-D] [-P SIZE]
  %(pgm)s [-vl] [-L LEVEL] [--LOG=DIR] [-c CONFIG] [-s SECTION] [-a ID]... [-d ID]... [-p PWFILE] [-D]
  %(pgm)s (-h | --help | -V | --version)

  There are no required options.

Options:
  -h, --help                     Show this help message and exit.
  -V, --version                  Show version information and exit.
  -f, --full                     Show all data, no filtering.
  -F FILTER, --filter=FILTER     Filter file to filter the data.
  -c CONFIG, --config=CONFIG     The configuration file.
                                 Default: "%(--config)s"
  -s SECTION, --section=SECTION  The configuration file version (default
                                 defined within the configuration file).
  -o OUTPUT, --output=OUTPUT     Output file or directory.
                                 Default: "%(--output)s"
  -p PWFILE, --pw=PWFILE         The password file.  This file is used when a
                                 login to a website or webpage is required.
                                 Default: "%(--pw)s"
  -l, --list                     List all of the IDs in the password file and
                                 exit.  If both the --list and --verbose
                                 options are included, list both IDs and
                                 Passwords and exit.
  -a ID, --add=ID                Add (or update) an ID and Password and exit.
                                 Program will prompt for the Password to be
                                 saved to the password file.
  -d ID, --delete=ID             Delete an ID (if it exists) from the
                                 password file and exit.
  -v, --verbose                  Print verbose messages.
  -L LEVEL, --log=LEVEL          Print log messages at log value LEVEL.
                                 Valid levels are: TRACE, DEBUG, INFO, WARNING,
                                 ERROR, and CRITICAL.
                                 Default: %(--log)s
  --LOG=DIR                      Log directory.
                                 Default: "%(--LOG)s"
  -D, --dryrun                   Only print out what would be done.
  -P SIZE, --poolsize=SIZE       Call OpenManage using pools of size SIZE.
                                 Default: set by the OS.
    """

    # Get current TOD.

    TOD = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Get default values.

    FQ_RUN_DIR = Path.cwd().resolve(strict=True)
    FQ_PGM_FILE = Path(__file__).resolve(strict=True)
    assert len(FQ_PGM_FILE.parts) >= 5
    PGM = Path(FQ_PGM_FILE.stem)
    FQ_BASE_DIR = FQ_PGM_FILE.parents[5]
    PKG = Path(__package__)

    ETC_DIR = Path("etc")
    OUTPUT_DIR = Path("output")
    LOG_DIR = Path("log")

    CONF_FILE = PGM.with_suffix(".yml")
    PASSWD_FILE = PGM.with_suffix(".pw")

    OUTPUT_FILE = Path(f"OpenManage-{PGM}.{TOD}.xlsx")
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

    PASSWD_LIST = [
        FQ_RUN_DIR / ETC_DIR / PKG / PASSWD_FILE,
        FQ_RUN_DIR / ETC_DIR / PASSWD_FILE,
        FQ_RUN_DIR / PASSWD_FILE,
        FQ_BASE_DIR / ETC_DIR / PKG / PASSWD_FILE,
        FQ_BASE_DIR / ETC_DIR / PASSWD_FILE,
        FQ_BASE_DIR / PASSWD_FILE
    ]

    for tmp in PASSWD_LIST:
        if tmp.is_file():
            FQ_PASSWD_FILE = tmp.resolve(strict=False)
            break
    else:
        print(f"Couldn't find Password File '{PASSWD_FILE.name}'.", file=sys.stderr)
        sys.exit(1)

    FQ_OUTPUT_DIR = (FQ_RUN_DIR / OUTPUT_DIR).resolve(strict=False)
    FQ_OUTPUT_FILE = (FQ_OUTPUT_DIR / OUTPUT_FILE).resolve(strict=False)

    FQ_LOG_DIR = (FQ_RUN_DIR / LOG_DIR).resolve(strict=False)
    FQ_LOG_FILE = (FQ_LOG_DIR / LOG_FILE).resolve(strict=False)

    help_arguments = {
        "pgm": PGM,
        "--config": FQ_CONF_FILE.file,
        "--LOG": FQ_LOG_FILE,
        "--log": "WARNING",
        "--output": FQ_OUTPUT_FILE,
        "--pw": FQ_PASSWD_FILE,
    }

    help_text = main.__doc__ % help_arguments

    pgm_version = f"{PGM}: {__package__}({ecscmdb.__version__}), ecspylibs({ecspylibs.__version__})"

    arguments = docopt(help_text, version=pgm_version)

    CONFIG = InitCheck(arguments, help_arguments, config="--config", section="--section")

    arguments = CONFIG.arguments
    data = CONFIG.data

    dry_run = arguments["--dryrun"]
    filter = arguments["--filter"]
    full = arguments["--full"]
    id_add = arguments["--add"]
    id_delete = arguments["--delete"]
    id_list = arguments["--list"]
    log_fd = arguments["--LOG"]
    log_level = arguments["--log"].upper()
    output = arguments["--output"]
    passwd_file = arguments["--pw"]
    pool_size = arguments["--poolsize"]
    verbose = arguments["--verbose"]
    version = arguments["--version"]

    ome_user = data["OME_Login"]

    output_file = CONFIG.output_file
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
    if verbose:
        print(f"\nStarting program {pgm_version}.\n", file=sys.stdout)

    if dry_run:
        print("\nList of command line arguments.\n", file=sys.stdout)

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
        print("\nList of all variables.\n", file=sys.stdout)

    for k, v in zip(my_locals_keys, my_locals_vals):
        logger.debug(f"{k:20} = '{v}'")
        if dry_run:
            print(f"{k:20} = '{v}'", file=sys.stdout)

    if dry_run:
        print("", file=sys.stdout)
        logger.info(f"Ending program {pgm_version}.")
        if verbose:
            print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
        sys.exit(0)

    if id_list or id_add or id_delete:
        logger.info("ID Maintenance.")
        passwd_data = Password(passwd_file)

        if id_add:
            logger.info("Add/Update ID.")
            for id in id_add:
                logger.debug(f"Add/Update ID {id}.")
                pw = getpass(prompt=f"Enter password for user '{id}': ")
                passwd_data.set(id, pw)
            del pw

        if id_delete:
            logger.info("Delete ID.")
            for id in id_delete:
                logger.debug(f"Delete ID {id}")
                passwd_data.delete(id)

        if id_list:
            logger.info("List IDs.")
            if verbose:
                passwd_data.list_pws()
            else:
                passwd_data.list_ids()

        del passwd_data
        logger.info(f"Ending program {pgm_version}.")
        if verbose:
            print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
        sys.exit(0)

    # The real stuff goes here.

    if filter:
        FILTER = ConfigFile(filter)
        FILTER_DATA = FILTER.read
        FILTER_SECTION = FILTER_DATA['section']
        FILTER_CONFIG = FILTER_DATA['config'][FILTER_SECTION - 1]

        FILTER_NAME = FILTER_CONFIG['name']
        FILTER_COLUMN_HEADER = FILTER_CONFIG['column_header']
        FILTER_RENAME_COLUMNS = FILTER_CONFIG['rename_columns']
        FILTER_SORT_COLUMNS = FILTER_CONFIG['sort_columns']

        NEW_FIELDS = []
        FILTER_ROWS = FILTER_CONFIG['filters']
        for i in FILTER_ROWS:
            row = i['row']
            columns = i['columns']
            if FILTER_COLUMN_HEADER not in columns:
                columns.append(FILTER_COLUMN_HEADER)
            if 'update' in i:
                update = i['update']
                for k in update.keys():
                    if k in columns:
                        columns.remove(k)
                    columns.append([k, update[k]])
            NEW_FIELDS.append([row, columns])
    else:
        FILTER_RENAME_COLUMNS = []
        FILTER_SORT_COLUMNS = []
        NEW_FIELDS = []
        full = True

    logger.info("Initialize the OpenManage REST API.")
    ome_api = API(ome_user, passwd_file)

    logger.info(f"login into the OpenManage REST API with with user '{ome_user}'.")
    ome_api.login()

    logger.info("Get list of all OpenManage devices.")
    df_device_list = ome_api.get_device_list()

    logger.debug(f"df_device_list = '{df_device_list}'.")

    logger.info("Initialize Pandas.")
    df_spreadsheet = pd.DataFrame()
    logger.info("Initialize ExcelWriter.")
    excel = pd.ExcelWriter(output)

    records_openmanage = {}
    records_inv_details = {}
    device_list = []
    device_id = {}

    logger.info("Create list of OpenManage devices.")
    if verbose:
        print("Create list OpenManage devices.", file=sys.stdout)

    for device in df_device_list["value"]:
        for device_mgt in device["DeviceManagement"]:
            for device_tag in ["DnsName", "MacAddress"]:
                if device_tag not in records_openmanage:
                    records_openmanage[device_tag] = []
                records_openmanage[device_tag].append(device_mgt[device_tag])

        for device_tag in ["DeviceName", "DeviceServiceTag", "Model", "InventoryDetails@odata.navigationLink"]:
            if device_tag not in records_openmanage:
                records_openmanage[device_tag] = []
            records_openmanage[device_tag].append(device[device_tag])

        device_name = device["DeviceName"][:31]
        id = device["Id"]
        model = device["Model"]

        device_list.append(device_name)
        device_id[device_name] = id

    logger.info("Create the VMWare worksheet.")
    if verbose:
        print("Create the VMWare worksheet.", file=sys.stdout)

    logger.info("Create df_spreadsheet from pd.DataFrame(records_openmanage).")
    df_spreadsheet = df_spreadsheet.append(pd.DataFrame(records_openmanage))

    logger.info("Sort df_spreadsheet.")
    df_spreadsheet = df_spreadsheet.sort_values(by=df_spreadsheet.columns.tolist())

    logger.info("Reindex df_spreadsheet.")
    df_spreadsheet = df_spreadsheet.reindex(sorted(df_spreadsheet.columns), axis=1)

    logger.info("Move column DnsName to column 1.")
    cols = df_spreadsheet.columns.tolist()
    cols.insert(0, cols.pop(cols.index("DnsName")))
    df_spreadsheet = df_spreadsheet.reindex(columns=cols)

    logger.info("Write df_spreadsheet to excel file as VMWare.")
    df_spreadsheet.to_excel(excel, "VMWare", index=False)

    logger.info("Update column widths of worksheet VMWare.")
    worksheet = excel.sheets["VMWare"]
    set_col_widths(worksheet, df_spreadsheet)

    device_list.sort()

    if full:
        logger.info("All Rows/Columns will be displayed.")

    else:
        logger.info("Configure which Rows and Columns to copy for each device type.")

        update_cells = UpdateCells()

        fields = NEW_FIELDS

    rename_columns = FILTER_RENAME_COLUMNS
    sort_field_names = FILTER_SORT_COLUMNS

    logger.info("Create a worksheet for each device.")
    if verbose:
        print("Create a worksheet for each device.", file=sys.stdout)

    device_count = 0
    device_length = len(device_list)

    logger.debug(f"Calling Parallel(ome_api.getInventoryDetails, process_pool=True, pool_size={pool_size})")
    if verbose:
        if pool_size:
            print(f"Creating {pool_size} pools to process {device_length} calls to the OpenManage REST API.", file=sys.stdout)
        else:
            print(f"Creating one pool per CPU to process {device_length} calls to the OpenManage REST API.", file=sys.stdout)

    try:
        get_inv_details = Parallel(ome_api.get_inventory_details, ProcessPoolExecutor, pool_size=pool_size)
    except Exception as e:
        logger.critical("Error processing ome_api.getInventoryDetails.  Process terminating.")
        logger.exception(f"Exception: {e=}")
        print("Error processing ome_api.getInventoryDetails.  Process terminating.", file=sys.stderr)
        sys.exit(1)

    logger.debug(f"{pool_size} pools created.")
    if verbose:
        if pool_size:
            print(f"{pool_size} pools created.", file=sys.stdout)
        else:
            print(f"One pool per CPU created.", file=sys.stdout)

    device_ids = list(device_id.values())
    logger.debug(f"{device_ids=}")

    logger.debug(f"Calling get_inv_details.run({device_ids})")
    if verbose:
        print(f"Calling OpenManage REST API with pool size of {pool_size} to retrieve {device_length} device records.", file=sys.stdout)

    try:
        results = get_inv_details.run(device_ids)
    except Exception as e:
        logger.critical(f"Error processing get_inv_details.run({device_ids}).  Process terminating.")
        logger.exception(f"Exception: {e=}")
        print(f"Error processing get_inv_details.run({device_ids}).  Process terminating.", file=sys.stderr)
        sys.exit(1)

    if verbose:
        print(
            f"The call to OpenManage took {get_inv_details.run_time:.2f} seconds",
            f"to fetch {device_length} OpenManage device records.",
            file=sys.stdout
        )
    logger.debug(f"get_inv_details.run took {get_inv_details.run_time} seconds to fetch {device_length} devices.")

    for result in results:
        id, data = result[0], result[1]
        logger.debug(f"{id=}")
        logger.debug(f"{type(data)=}")
        if data:
            logger.debug(f"Found data for id '{id}'.")
            records_inv_details[id] = data
        else:
            logger.error(f"Did not find data for id '{id}'.")
            print(f"Error processing get_inv_details.run({device_ids}).  Process terminating.", file=sys.stderr)
            sys.exit(1)

    for device in device_list:
        device_count += 1
        id = device_id[device]

        logger.info(f"Creating worksheet[{device_count}:{device_length}] for device '{device}[{id}]'.")
        if verbose:
            print(f"Creating worksheet[{device_count}:{device_length}] for device '{device}[{id}]'.", file=sys.stdout)
        if id in records_inv_details:
            logger.debug(f"records_inv_details[{id}] : {records_inv_details[id]}")
        else:
            logger.error(f"Couldn't find id '{id}' in records_inv_details.")
            print("Error processing Detail records.  Process terminating.", file=sys.stderr)
            sys.exit(1)

        df_inv_details = pd.read_json(records_inv_details[id])
        logger.debug(f"df_inv_details : {df_inv_details}")
        logger.debug(f"df_inv_details['value'] : {df_inv_details['value']}")
        sheet = json_normalize(df_inv_details["value"], "InventoryInfo", ["InventoryType"])

        if not full:
            logger.info(f"If device '{device}' is a server or enclosure, filter out unnecessary data.")

            out_fields = {}

            for row, columns in fields:
                logger.info(f"Looking for row '{row}' for device '{device}'.`")

                if sheet["InventoryType"].str.contains(row).any():
                    logger.info(f"Found row '{row}' for device '{device}'.`")

                    if row not in out_fields:
                        out_fields[row] = []

                    for column in columns:
                        if type(column) is list:
                            column, cmd = column
                        else:
                            cmd = None

                        logger.info(f"Looking for row:column '{row}:{column}' for device '{device}'.")

                        if column in sheet.columns:
                            logger.info(f"Found row:column '{row}:{column}' for device '{device}'.`")
                            out_fields[row].append(column)
                            logger.debug(f"out_fields[{row}] : {out_fields[row]}")

                        else:
                            logger.info(f"Can't find row:column '{row}:{column}' for device '{device}'.`")

                else:
                    logger.info(f"Can't find row '{row}' for device '{device}'.")

            out = {}

            for key in out_fields.keys():
                logger.debug(f"out_fields[{key}] : '{out_fields[key]}'")
                out[key] = sheet.loc[(sheet["InventoryType"] == key), out_fields[key]]

            logger.info(f"Recreate sheet for device '{device}'.")
            sheet = pd.concat([out[key] for key in out], sort=False)

            logger.debug(f"Sheet = '{sheet}'.")

            for row, columns in fields:
                logger.info(f"Looking for row '{row}' for device '{device}'.`")

                if sheet["InventoryType"].str.contains(row).any():
                    logger.info(f"Found row '{row}' for device '{device}'.`")

                    for column in columns:
                        if type(column) is list:
                            column, cmd = column
                        else:
                            continue

                        logger.info(f"Looking for row:column '{row}:{column}' for device '{device}'.")

                        if column in sheet.columns:
                            logger.info(f"Found row:column '{row}:{column}' for device '{device}'.`")
                            if not update_cells.run(cmd, sheet):
                                logger.error(f"Error calling update_cell('{cmd}', {device})")
                                print(f"Error updating cell information using module '{cmd}' for sheet {device}.", file=sys.stderr)
                                sys.exit(1)
                else:
                    logger.info(f"Can't find row '{row}' for device '{device}'.")

            logger.info(f"Rename, if necessary, column names for device '{device}'.")
            logger.debug(f"{rename_columns=}")
            sheet = sheet.rename(columns=rename_columns)

        logger.info(f"Sort the columns for sheet '{device}'.")
        sheet = sheet.reindex(sorted(sheet.columns), axis=1)

        logger.info(f"Move column 'InventoryType' to the beginning of the spreadsheet for device '{device}'.")
        cols = sheet.columns.tolist()
        logger.debug(f"sheet : {sheet}")
        logger.debug(f"sheet.columns : {sheet.columns}")
        logger.debug(f"sheet.columns.tolist() : {sheet.columns.tolist()}")
        cols.insert(0, cols.pop(cols.index("InventoryType")))
        sheet = sheet.reindex(columns=cols)

        sort_fields = []
        logger.debug(f"sort_field_names = {sort_field_names}")

        for field_name in sort_field_names:
            logger.debug(f"field_name = {field_name}")
            logger.debug(f"Is '{field_name}' in {sheet.columns.tolist()}")
            if field_name in sheet.columns:
                if field_name not in sort_fields:
                    logger.debug(f"Add '{field_name}' to {sort_fields}")
                    sort_fields.append(field_name)
                else:
                    logger.debug(f"'{field_name}' already in {sort_fields}")

        if sort_fields:
            logger.debug(f"'{device}.sort_fields' = {sort_fields}")
            sheet.sort_values(by=sort_fields, inplace=True, ignore_index=True)

        logger.info(f"Update the spreadsheet for device {device}.")
        sheet.to_excel(excel, device, index=False)

        worksheet = excel.sheets[device]
        set_col_widths(worksheet, sheet)

    logger.info("Save and close the spreadsheet file.")
    if verbose:
        print("Save and close the spreadsheet file.", file=sys.stdout)
    excel.save()
    excel.close()

    rc = ReapChildren()
    try:
        rc.reapChildren()
    except Exception as e:
        logger.critical("Fatal error occurred in reapChildren().")
        logger.exception(f"Exception: '{e}'.")

    logger.info(f"Ending program {pgm_version}.")
    if verbose:
        print(f"\nEnding program {pgm_version}.\n", file=sys.stdout)
