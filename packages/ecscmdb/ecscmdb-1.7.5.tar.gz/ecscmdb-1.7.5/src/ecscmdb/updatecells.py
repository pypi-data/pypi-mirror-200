#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Fri Feb 17 12:54:13 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $
#

from autologging import logged, traced
from pandas import json_normalize
from dataclasses import dataclass

@traced
@logged
@dataclass
class UpdateCells:
    """Update cells."""

    def __post_init__(self):
        self.modules = {
            "update_ports": self.update_ports,
            "update_end_point_agents": self.update_end_point_agents,
        }
        self.end_point_agents = None
        self.cols = None
        self.macs = None
        self.partitions = None

    def run(self, module: str, sheet: object) -> bool:
        self.__log.info(f"In UpdateCells.run('{module}', '{sheet}')")
        if module in self.modules:
            self.__log.info(f"Calling UpdateCells.{module}('{sheet}')")
            self.modules[module](sheet)
        else:
            self.__log.error(f"Module 'UpdateCells.{module}' not found.")
            return False
        return True

    def update_ports(self, sheet: object) -> None:
        for self.i in sheet.loc[sheet["InventoryType"].str.contains("serverNetworkInterfaces")].index:
            self.partitions = json_normalize(sheet.loc[self.i, "Ports"], "Partitions")
            self.__log.debug(f"Partitions : {self.partitions}")

            for self.debugName in self.partitions:
                self.__log.debug(f"Partition Name : {self.debugName}")

            if "CurrentMacAddress" in self.partitions:
                self.macs = []
                for self.mac in self.partitions.CurrentMacAddress:
                    self.__log.debug(f"Mac Address : {self.mac}")
                    self.macs.append(self.mac)
                sheet[f"Ports.CurrentMacAddress"] = ""
                sheet.at[self.i, "Ports.CurrentMacAddress"] = self.macs

        self.cols = sheet.columns.tolist()
        self.__log.debug(f"Columns before delete Ports: {self.cols}")

        self.__log.info(f"Delete column 'Ports'.")
        sheet.drop("Ports", axis=1, inplace=True)

        self.cols = sheet.columns.tolist()
        self.__log.debug(f"Columns after delete Ports: {self.cols}")

    def update_end_point_agents(self, sheet: object) -> None:
        for self.i in sheet.loc[sheet["InventoryType"].str.contains("deviceManagement")].index:
            self.end_point_agents = json_normalize(sheet.loc[self.i, "EndPointAgents"])
            self.__log.debug(f"endPointAgents : {self.end_point_agents}")
            self.__log.debug(f"endPointAgents.columns : {self.end_point_agents.columns}")

            for self.column in self.end_point_agents.columns:
                self.__log.info(f"endPointAgents.column : {self.column}")
                self.__log.debug(f"endPointAgents.{self.column} : {self.end_point_agents[self.column]}")
                self.__log.debug(f"endPointAgents.{self.column}.values : {self.end_point_agents[self.column].values}")
                self.__log.debug(f"Type(endPointAgents.{self.column}.values) : {type(self.end_point_agents[self.column].values)}")

                self.__log.info(f"Try to sort endPointAgents.{self.column}.values.")
                self.__log.debug(f"endPointAgents.{self.column}.values before {self.end_point_agents[self.column].values}")
                try:
                    self.end_point_agents[self.column].values.sort()
                    self.__log.debug(f"endPointAgents.{self.column}.values after {self.end_point_agents[self.column].values}")
                except Exception as e:
                    self.__log.warning(f"Couldn't sort 'endPointAgents.{self.column}.values'.")
                    self.__log.exception(f"Exception: '{e}'.")

                sheet[f"EndPointAgents.{self.column}"] = ""
                sheet.at[self.i, f"EndPointAgents.{self.column}"] = self.end_point_agents[self.column].values

        self.cols = sheet.columns.tolist()
        self.__log.debug(f"Columns before delete EndPointAgents: {self.cols}")

        self.__log.info(f"Delete column 'EndPointAgents'.")
        sheet.drop("EndPointAgents", axis=1, inplace=True)

        self.cols = sheet.columns.tolist()
        self.__log.debug(f"Columns after delete EndPointAgents: {self.cols}")
