"""
project.py
================================================
The core module for the Project class.

"""

import os
import yaml
import hashlib
from os import path
import pandas as pd

from nsaphx.log import LOGGER
from nsaphx.database import Database
from nsaphx.data_node import MainDataNode


class Project:
    """ Project Class
    The Project class generates a project object with collecting the project's
    details. 

    Parameters
    ----------
    project_params : dict
    The parameters of the project. It should contain the following mandotary 
    keys:

    | name: str
    | project_id: int
    | data.outcome_path: str
    | data.exposure_path: str
    | data.covariate_path: str

    Notes
    -----
    The project object does not load the data. It only stores the paths to the 
    data. Other than mandatory keys, the project_params can contain other keys. 

    Examples
    --------

    >>> from nsaphx.project import Project
    >>> project_params = {"name": "test_project", "project_id": 1,
                          "data": {"outcome_path": "data/outcome.csv", 
                                   "exposure_path": "data/exposure.csv", 
                                   "covariate_path": "data/covariate.csv"}}
    >>> project = Project(project_params = project_params, db_path = "test.db")
    """

    def __init__(self, project_params, db_path):
        
        self.project_params = project_params
        self._check_params()
        self.pr_name = self.project_params.get("name")
        self.pr_id = self.project_params.get("project_id")
        self.db_path = db_path
        self.hash_value = None
        self.gps_list = list()
        self._add_hash()
        self.db = None
        self._connect_to_database()
        self._main_data_node = None
        self._add_main_data_node()

    def _check_params(self):
        #TODO: In case of raising exceptions, refer the users to the documentation.
        
        required_keys = ["name", "project_id", "data"]
        required_data_keys = ["outcome_path", "exposure_path", "covariate_path"]

        for key in required_keys:
            if key not in self.project_params.keys():
                raise KeyError(f"In the project.yaml file, " \
                                f"please provide the '{key}' field.")
        for key in required_data_keys:
            if key not in self.project_params.get("data").keys():
                raise KeyError(f"In the project.yaml file, "\
                                f"under the 'data' field, " \
                                f"please provide the '{key}' field.")

    def _connect_to_database(self):
        if self.db_path is None:
            raise Exception("Database is not defined.")
            
        self.db = Database(self.db_path)

    def ping_data(self):
        # This includes checking if the data is still accessible. 
        # if the format is supported.
        # if each data comes with id column.
        raise NotImplementedError


    def __str__(self) -> str:

        return (f"Project name: {self.pr_name} \n"
               f"Project id: {self.pr_id} \n"
               f"Project database: {self.db_path} \n")


    def __repr__(self) -> str:
        return (f"Project({self.pr_name})")

    def _add_hash(self):
        
        # check the yaml file --------------------------------------------------
        if ("name" not in self.project_params.keys() or 
            self.project_params.get("name") is None):

            raise KeyError("Please provide a 'name' field"
                           + " in the project.yaml file.")


        if ("project_id" not in self.project_params.keys() or 
            self.project_params.get("project_id") is None):

            raise KeyError("Please provide a 'project_id' field"
                           + " in the project.yaml file.")

        if ("data" not in self.project_params.keys() or 
            self.project_params.get("data").get("outcome_path") is None or 
            self.project_params.get("data").get("covariate_path") is None or
            self.project_params.get("data").get("exposure_path") is None):

            raise KeyError("Please provide the 'outcome_path', " 
                           + "'covariate_path', and 'exposure_path' fields in " 
                           + " the project.yaml file.")

        # create a hash string 
        outcome_path = self.project_params.get("data").get("outcome_path")
        exposure_path = self.project_params.get("data").get("exposure_path")
        covariate_path = self.project_params.get("data").get("covariate_path")

        outcome_name = path.basename(outcome_path).split('/')[-1]
        exposure_name = path.basename(exposure_path).split('/')[-1]
        covariate_name = path.basename(covariate_path).split('/')[-1]

        hash_string = "-".join([str(self.project_params.get("name")), 
                                str(self.project_params.get("id")), 
                                outcome_name, exposure_name, covariate_name])

        try:            
            self.hash_value =  hashlib.sha256(
                hash_string.encode('utf-8')).hexdigest()
        except Exception as e:
            print(e) 

        self.project_params["hash_value"] = self.hash_value

    def summary(self):
        if len(self.gps_list) == 0:
            print ("The project does not have any computed GPS object.")
        else:
            print(f"The project has {len(self.gps_list)} GPS object(s): ")
            for item in self.gps_list:
                gps = self.db.get_value(item)
                print(gps)

    def _add_main_data_node(self):
        """Add the main data node to the database.
        """
        if self._main_data_node is None:
            # Generate main data node and add to the database.
            main_data_node = MainDataNode(self.project_params,
                                          db_path=self.db_path)
            self._main_data_node = main_data_node.hash_value
            self.db.set_value(self._main_data_node, main_data_node)

        else:
            # Retrieve the main data node from the database.
            self.db.set_value(self.hash_value, self)   

    def get_data_node(self):
        return self.db.get_value(self._main_data_node)

if __name__ == "__main__":
    pass