#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Thu Mar 23 18:14:14 2023 -0400 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $
#

# Python Standard libraries.

import sys
import pandas as pd

from autologging import logged, traced


@traced
@logged
class FindDifferences:
    """Update cells."""

    def __init__(self, df1: object, df2: object, df_comments: object):
        """ blah """

        self.df1 = df1
        self.df2 = df2
        self.df_comments = df_comments
        self.__log.debug(f"On enter '{self.df_comments=}'")

        self.colors = {
            "blue": "background-color: blue; font-weight: bold",
            "green": "background-color: green; font-weight: bold",
            "red": "background-color: red; font-weight: bold",
            "yellow": "background-color: yellow; font-weight: bold",
        }

    def find_differences(self, sheet: object) -> list:
        """ blah """

        df1_sheet = self.df1[sheet]
        df2_sheet = self.df2[sheet]

        df_style = pd.DataFrame("", index=df2_sheet.index, columns=df2_sheet.columns)

        columns1 = set(df1_sheet.columns.to_list())
        columns2 = set(df2_sheet.columns.to_list())

        columns_deleted = list(columns1.difference(columns2))
        columns_added = list(columns2.difference(columns1))
        columns_common = list(columns1.intersection(columns2))

        if not df1_sheet.equals(df2_sheet):
            self.__log.debug("df1_sheet != df2_sheet")
            for column in columns_common:
                self.__log.debug(f"{column=}")
                if not df1_sheet[column].equals(df2_sheet[column]):
                    for row in df1_sheet[df2_sheet[column].ne(df1_sheet[column]) == True].index.to_list():
                        max_rows_df1_sheet = df1_sheet.shape[0]
                        max_rows_df2_sheet = df2_sheet.shape[0]

                        self.__log.debug(f"{row=}")
                        self.__log.debug(f"{max_rows_df1_sheet=}")
                        self.__log.debug(f"{max_rows_df2_sheet=}")

                        if row < max_rows_df1_sheet and row < max_rows_df2_sheet:
                            value1 = df1_sheet.at[row, column]
                            value2 = df2_sheet.at[row, column]

                            self.__log.debug(f"{value1=}")
                            self.__log.debug(f"{value2=}")

                            self.df_comments = self.df_comments.append(
                                {
                                    "Summary of changes.": f"Cell [{column}, {row + 2}] in sheet '{sheet}' changed (listed in yellow).",
                                    "See sheet tab for details.": f"{sheet}",
                                }, ignore_index=True)

                            df2_sheet.at[row, column] = f"\"{value1}\" -> \"{value2}\""
                            df_style.at[row, column] = self.colors["yellow"]
                        else:
                            if row >= max_rows_df1_sheet:
                                self.__log.debug(f"{row=} >= {max_rows_df1_sheet=}")
                                self.df_comments = self.df_comments.append(
                                    {
                                        "Summary of changes.": f"Row {row + 2} was added to '{sheet}'.",
                                        "See sheet tab for details.": f"{sheet}",
                                    }, ignore_index=True)

                            if row >= max_rows_df2_sheet:
                                self.__log.debug(f"{row=} >= {max_rows_df2_sheet=}")
                                self.df_comments = self.df_comments.append(
                                    {
                                        "Summary of changes.": f"Row {row + 2} was removed to '{sheet}'.",
                                        "See sheet tab for details.": f"{sheet}",
                                    }, ignore_index=True)

                                # self.__log.info(f"Adding row to df2_sheet.")
                                # df2_sheet = df2_sheet.append(df1_sheet.iloc[row])
                                # df_style = df_style.append(self.colors["red"])

            if columns_deleted or columns_added:
                self.__log.debug(f"{columns_deleted=} or {columns_added=}")
                if columns_added:
                    self.__log.debug(f"{columns_added=}")
                    if len(columns_added) == 1:
                        self.df_comments = self.df_comments.append(
                            {
                                "Summary of changes.": f"Column {columns_added} was added to sheet '{sheet}' (listed in green).",
                                "See sheet tab for details.": f"{sheet}",
                            }, ignore_index=True)
                    else:
                        self.df_comments = self.df_comments.append(
                            {
                                "Summary of changes.": f"Columns {columns_added} were added to sheet '{sheet}' (listed in green).",
                                "See sheet tab for details.": f"{sheet}",
                            }, ignore_index=True)

                    for column in columns_added:
                        df_style[column] = self.colors["green"]

                if columns_deleted:
                    self.__log.debug(f"{columns_deleted=}")
                    if len(columns_deleted) == 1:
                        self.df_comments = self.df_comments.append(
                            {
                                "Summary of changes.": f"Column {columns_deleted} was deleted from sheet '{sheet}' (listed in red).",
                                "See sheet tab for details.": f"{sheet}",
                            }, ignore_index=True)
                    else:
                        self.df_comments = self.df_comments.append(
                            {
                                "Summary of changes.": f"Columns {columns_deleted} were deleted from sheet '{sheet}' (listed in red).",
                                "See sheet tab for details.": f"{sheet}",
                            }, ignore_index=True)

                    for column in columns_deleted:
                        df2_sheet[column] = df1_sheet[column]
                        df_style[column] = self.colors["red"]

        if sheet == "VMWare":
            column_header = "DnsName"
        else:
            column_header = "InventoryType"

        self.__log.info(f"Resort df2_sheet.")
        df2_sheet = df2_sheet.reindex(sorted(df2_sheet.columns), axis=1)
        cols = df2_sheet.columns.tolist()
        cols.insert(0, cols.pop(cols.index(column_header)))
        df2_sheet = df2_sheet.reindex(columns=cols)

        self.__log.info(f"Resort df_style.")
        df_style = df_style.reindex(sorted(df_style.columns), axis=1)
        cols = df_style.columns.tolist()
        cols.insert(0, cols.pop(cols.index(column_header)))
        df_style = df_style.reindex(columns=cols)

        self.__log.info(f"Return [df_style, df2_sheet, self.df_comments].")
        self.__log.debug(f"On exit '{self.df_comments=}'")
        return [df_style, df2_sheet, self.df_comments]

    def set_style(self, df: object, style: object = None) -> object:
        """ blah """

        return style
