"""
data_node.py
============
The core module for the MainDataNode and DataNode classes.

"""

import json
import hashlib
from abc import ABC, abstractmethod
from nsaphx.plugin_registery import PLUGIN_MAP
from nsaphx.database import Database
import os
from nsaphx.base.utils import human_readible_size
import re
import pandas as pd
import warnings
from functools import reduce
from nsaphx.base.discovery import Graph, Node, print_graph

class DataClass(ABC):
    """ DataClass
    The DataClass is an abstract class for the MainDataNode and DataNode classes.
    It contains the common attributes and methods for the two classes.
    """

    @abstractmethod
    def _add_hash(self):
        pass

    @abstractmethod
    def check_data(self):      
        pass    

    def apply(self, instruction):
        # Generates a new lazy node and put's it in the data.base.
        if not self.computed:
            warnings.warn("The data node has not been computed yet. ")
            return
        
        plugin_name = instruction.get("plugin_name")
        plugin_function = PLUGIN_MAP.get(plugin_name)

        if plugin_function is not None:
            data_node = DataNode(self.hash_value, instruction,
                                 db_path=self.db_path)
            if data_node.hash_value in self.descendant_hash:
                data_node = self.db.get_value(data_node.hash_value)
                print(f"Data node was retrieved from database.")
            else:
                data_node.input_data = self.output_data
                self.descendant_hash.append(data_node.hash_value)
                if self.hash_by_type.get(plugin_name) is None:
                    self.hash_by_type[plugin_name] = [data_node.hash_value]
                else:
                    self.hash_by_type[plugin_name].append(data_node.hash_value)
                self.db.set_value(data_node.hash_value, data_node)
                self.db.set_value(self.hash_value, self)
            return data_node
        else:
            raise ValueError(f"Plugin {plugin_name} not found.")

    def summary(self):
        print(f"Data node hash: {self.hash_value}")
        print(f"    Data:")
        for key, value in self.input_data["path"].items():
            print(f"        {key}: {value}")
        if (self.input_data["d_index"] is None): 
            index_len  = None
        else:
            index_len = len(self.input_data["d_index"])
        print(f"    Index filtering length: {index_len}")
        print(f"    Number of decendent nodes: {len(self.descendant_hash)}")
        if len(self.descendant_hash) > 0:
            print(f"    Hash by type: ")
            for key, value in self.hash_by_type.items():
                if len(value) > 0:
                    print(f" "*8 + f"{key}")
                    for v in value:
                        print(f" "*12 + f"{v}")

    def __str__(self):
        return (f"{self.__class__.__name__}(hash_value={self.hash_value}," + 
                f" db_path={self.db_path})")
    
    def instruction_summary(self):
        print(f"Data node hash: {self.hash_value}")
        print(f"    Instruction:")
        for key, value in self.instruction.items():
            print(f"        {key}: {value}")
        input_data_len = len(self.input_data.get("d_index"))
        output_data_len = len(self.output_data.get("d_index"))
        print(f"    input data size: {input_data_len}")
        print(f"    output data size: {output_data_len}")
        print(f"    computed: {self.computed}")
        
class MainDataNode(DataClass):
    """ MainDataNode
    The MainDataNode is the first node in the data pipeline. User can apply 
    instructions to the MainDataNode to generate a new DataNode. Each project
    has one MainDataNode object.

    Parameters
    ----------
    project_params : dict
        A dictionary containing the project parameters.
    db_path : str
        The path to the database file.
    """
    def __init__(self, project_params, db_path):
        self.project_params = project_params
        self.input_data = None
        self.output_data = None
        self.computed = True
        self.hash_value = None
        self.node_id = None
        self._add_hash()
        self._create_data_attribute()
        self.descendant_hash = []
        self.hash_by_type = dict()
        self.db_path = db_path
        self._connect_to_database()

    def _create_data_attribute(self):
        data_path_keys = ["exposure_path", "outcome_path", "covariate_path"]
        self.input_data = {"path": {}, "d_index": None}
        for key in data_path_keys:
            value = self.project_params.get("data").get(key)
            self.input_data["path"][key] = value
        
        _data = []
        for _ , path_value in self.input_data.get("path").items():
             _data.append(pd.read_csv(path_value))
        merged_df = reduce(lambda left,
                           right: pd.merge(left, right, on='id'), _data)
        
        d_index = merged_df["id"].tolist()
        self.input_data["d_index"] = d_index
        
        self.output_data = self.input_data
        
    def _add_hash(self):
        hash_string = self.project_params["hash_value"] + "MainDataNode"
        try:            
            self.hash_value =  hashlib.sha256(
                hash_string.encode('utf-8')).hexdigest()
            self.node_id = hashlib.shake_256(self.hash_value.encode()).hexdigest(8)
        except Exception as e:
            print(e) 

    def data_summary(self):
        self.check_data()
        for key, value in self.input_data["path"].items():
            print(f"{re.sub('_path', '', key)}:")
            key_data = pd.read_csv(value)
            print(f"    Number of rows: {key_data.shape[0]}")
            print(f"    Number of columns: {key_data.shape[1]}")
            print(f"    Column names: {key_data.columns.tolist()}")
            print(f"    First 5 rows:")
            print(key_data.head())

    def access_data(self, data_name = None):
        """access_data
        Access the data in the data node. If data_name is None, return a
        dictionary containing all the data. Otherwise, return the data
        specified by data_name.

        Parameters
        ----------
        data_name : str, optional
            The name of the data to be returned, by default None
        
        Returns
        -------
        data : dict
            A dictionary containing the requested data in the data node.
        """
        
        if data_name is None:
            data = {}
            for key, value in self.input_data["path"].items():
                _key = f"{re.sub('_path', '', key)}"
                loaded_data = pd.read_csv(value)
                data[_key] = loaded_data
        else:
            raise NotImplementedError("Accessing data by name is not implemented yet.")

        return data

    def _connect_to_database(self):
        """_connect_to_database
        Connect to the database.
        """
        if self.db_path is None:
            raise Exception("No database path provided.")
        
        self.db = Database(self.db_path)

    def get_data_node(self, hash_value):
        # TBD - Maybe is not needed
        return self.db.get_value(hash_value)
    
    def check_data(self):
        """ check_data 
        Check if the data files are accessible and print out the file size.
        """
        for key, value in self.input_data["path"].items():
            print(f"Working on {key} : {value} ...")
            file_exist = os.path.exists(value)
            print(f"    File accessible: {file_exist}")
            if file_exist:
                file_size = human_readible_size(os.path.getsize(value))
                print(f"    File size: {file_size}")

    def apply_instruction_chain(self, instruction_list):
        """apply_instruction_chain
        Apply a list of instructions to the MainDataNode to generate a sequence
        of new DataNodes.
        """
        my_node = self
        for instruction in instruction_list:
            my_node = my_node.apply(instruction)
            my_node.compute()
        return my_node
        

class DataNode(DataClass):
    """DataNode
    The DataNode is the basic unit in the data pipeline. User can apply 
    instructions to the DataNode to generate a new DataNode. Each DataNode
    has a parent DataNode and can have one or more decendant DataNodes.

    Parameters
    ----------
    parent_node_hash : str
        The hash value of the parent DataNode.
    instruction : dict
        The instruction to be applied to the node. 
    db_path : str
        The path to the database file.

    Attributes
    ----------
    input_data : dict
        The input data of the node.
    output_data : dict
        The output data of the node.
    computed : bool
        Whether the node has been computed.
    hash_value : str
        The hash value of the node.
    node_id : str
        The node id of the node (This is a shortened hash value.)
    parent_node_hash : str
        The hash value of the parent DataNode (or MainDataNode).
    instruction : dict
        The instruction to be applied to the node.
    db_path : str
        The path to the database file.
    descendant_hash : list
        A list of hash values of the decendant DataNodes.
    hash_by_type : dict
        A dictionary containing the hash values of the decendant DataNodes that 
        is grouped by the type of the DataNode.
    db : Database
        The database object.
    """
    def __init__(self, parent_node_hash, instruction, db_path):
        self.input_data = None
        self.output_data = None
        self.computed = False
        self.hash_value = None
        self.node_id = None
        self.parent_node_hash = parent_node_hash
        self.instruction = instruction
        self.db_path = db_path
        self.descendant_hash = []
        self.hash_by_type = dict()
        self._connect_to_database()
        self._update_input_data()
        self._add_hash()

    def _add_hash(self):
        """_add_hash
        Add the hash value and node_id to the node.
        """
        hash_string = (self.parent_node_hash + 
                       json.dumps(self.instruction, sort_keys=True))
        
        self.hash_value = hashlib.sha256(
            hash_string.encode('utf-8')).hexdigest()
        self.node_id = hashlib.shake_256(self.hash_value.encode()).hexdigest(8)

    def compute(self):
        """compute
        Compute the node. This function will call the plugin function to
        compute the node and update the node on the database.
        """
        if self.computed is False:
    
            # compute
            self.computed = True
            plugin_name = self.instruction.get("plugin_name")
            plugin_function = PLUGIN_MAP.get(plugin_name)
            
            if plugin_function is not None:
                output_data = plugin_function(self.input_data, self.instruction)
                # sanity check to see if output data has required keys.
                self.output_data = output_data
                self.update_node_on_db()
            else:
                raise ValueError(f"Plugin {plugin_name} not found.")
            
        else:
            print(f"The data node has already been computed." +
                  f"Run .reset() to reset the node.")
            
    def reset(self):
        """reset
        Reset the node. This function will reset the node to the state before
        it is computed.
        """
        self.computed = False
        self._update_input_data()

    def _update_input_data(self):
        """_update_input_data
        Update the input data of the node. This function will get the output
        data of the parent node and set it as the input data of the node. The 
        current node will be updated on the database.
        """
        parent_node = self.db.get_value(self.parent_node_hash)
        self.input_data = parent_node.output_data 
        self.update_node_on_db()

    def _connect_to_database(self):
        """_connect_to_database
        Connect to the database.
        """
        if self.db_path is None:
            raise Exception("No database path provided.")
        
        self.db = Database(self.db_path)

    def update_node_on_db(self):
        """update_node_on_db 
        Update the node on the database.
        """
        self.db.set_value(self.hash_value, self)
    
    def check_data(self):
        """check_data
        Check the data of the node. This function will check if the data
        files are accessible and print out the file size.
        """
        for key, value in self.input_data["path"].items():
            print(f"Working on {key} : {value} ...")
            file_exist = os.path.exists(value)
            print(f"    File accessible: {file_exist}")
            if file_exist:
                file_size = human_readible_size(os.path.getsize(value))
                print(f"    File size: {file_size}")

    def access_input_data(self, data_name = None):
        """access_input_data
        Access the input data of the node. This function will load the data
        from the data files and return a dictionary containing the data.

        Parameters
        ----------
        data_name : str, optional
            The name of the data to be accessed. If None, all data will be
            accessed. (default: None)
        """
        if data_name is None:
            data = {}
            for key, value in self.input_data["path"].items():
                _key = f"{re.sub('_path', '', key)}"
                loaded_data = pd.read_csv(value)
                if self.input_data["d_index"] is not None:
                    selected_data = loaded_data[loaded_data["id"].isin(self.input_data["d_index"])]
                else:
                    selected_data = loaded_data
                data[_key] = selected_data
        else:
            raise NotImplementedError("Accessing data by name is not implemented yet.")

        return data

    def access_output_data(self, data_name = None):
        """access_output_data
        Access the output data of the node. This function will load the data
        from the data files and return a dictionary containing the data.

        Parameters
        ----------
        data_name : str, optional
            The name of the data to be accessed. If None, all data will be
            accessed. (default: None)
        """
        if data_name is None:
            data = {}
            for key, value in self.output_data["path"].items():
                _key = f"{re.sub('_path', '', key)}"
                loaded_data = pd.read_csv(value)
                if self.output_data["d_index"] is not None:
                    selected_data = loaded_data[
                        loaded_data["id"].isin(self.output_data["d_index"])]
                else:
                    selected_data = loaded_data
                data[_key] = selected_data
        else:
            raise NotImplementedError("Accessing data by name is not implemented yet.")

        return data



    def history(self, detail = False):

        nodes = [self]
        node = self

        while True:
            if node.parent_node_hash is None:
                break
            else:
                node = self.db.get_value(node.parent_node_hash)
                nodes.append(node)    
            if isinstance(node, MainDataNode):
                break

        nodes = nodes[::-1]

        if detail:
            for node in nodes:
                if isinstance(node, MainDataNode):
                    print(f"Main data node: {node}")
                else:
                    node.instruction_summary()
        else:
            for i, node in enumerate(nodes):
                if i == len(nodes) - 1:
                    print(f"You are here -> {node}")
                else:
                    print(node)

    def create_descendant_graph(self, graph = None):
        if graph is None:
            graph = Graph()
        elif not isinstance(graph, Graph):
            raise ValueError("graph must be a Graph object.")
    
        node_a = None
        for node in graph.nodes:
            if node.val == self.hash_value:
                node_a = node
                break

        if node_a is None:
            node_a = Node(val=self.hash_value)
            graph.add_node(node_a)
    
        for descendant_hash in self.descendant_hash:
            descendant_node = self.db.get_value(descendant_hash)
            node_b = None
            for node in graph.nodes:
                if node.val == descendant_hash:
                    node_b = node
                    break
            if node_b is None:
                node_b = Node(val=descendant_hash)
                graph.add_node(node_b)
            graph.add_connection(node_a, node_b)
            graph = descendant_node.create_descendant_graph(graph=graph)
    
        return graph

    def decendents(self, detail = False):
        
        if detail:
            pass
        else:
            graph = self.create_descendant_graph()
            graph.print_graph()



    