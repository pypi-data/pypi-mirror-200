import pandas as pd
from functools import reduce
from nsaphx.base.utils import check_instruction_keys

def filter_plugin(input_data, instruction):
    """
    Filter the data based on the instruction.
    """
    # sanity checks -----------------------------------------------------------
    if instruction.get("plugin_name") != "filter":
        raise ValueError("Plugin name does not match.")
    
    required_instruction_keys = ["plugin_name", "filter_condition"]
    check_instruction_keys(required_instruction_keys, instruction)

    # -------------------------------------------------------------------------

    # Step 1: load the data
    _data = []
    # Get the names of the dataframes
    df_names = [key for key in input_data.get("path")]

    for _ , path_value in input_data.get("path").items():
         _data.append(pd.read_csv(path_value))
    
    # Step 2: merge data
    merged_df = reduce(lambda left,
                        right: pd.merge(left, right, on='id'), _data)

    if input_data.get("d_index") is not None:
        merged_df = merged_df[merged_df["id"].isin(input_data.get("d_index"))]
    
    # Step 3: filter data
    filtered_data = merged_df.query(instruction.get("filter_condition"))

    # Step 4: get the index of the filtered data
    d_index = filtered_data["id"].tolist()
     
    
    # Step 5: The following is the same for all plugins
    output_data = {"path" : input_data.get("path"),
                   "d_index" : d_index,
                   "d_generated" : {}}

    return output_data



def drop_na(input_data, instruction):
    """
    Drop the rows that contain NaN values.
    """
    # sanity checks -----------------------------------------------------------
    if instruction.get("plugin_name") != "drop_na":
        raise ValueError("Plugin name does not match.")
    
    required_instruction_keys = ["plugin_name"]
    check_instruction_keys(required_instruction_keys, instruction)

    # -------------------------------------------------------------------------

    # Step 1: load the data
    _data = []
    # Get the names of the dataframes
    df_names = [key for key in input_data.get("path")]

    for _ , path_value in input_data.get("path").items():
         _data.append(pd.read_csv(path_value))
    
    # Step 2: merge data
    merged_df = reduce(lambda left,
                        right: pd.merge(left, right, on='id'), _data)

    if input_data.get("d_index") is not None:
        merged_df = merged_df[merged_df["id"].isin(input_data.get("d_index"))]
    
    # Step 3: filter data
    filtered_data = merged_df.dropna()

    # Step 4: get the index of the filtered data
    d_index = filtered_data["id"].tolist()
     
    
    # Step 5: The following is the same for all plugins
    output_data = {"path" : input_data.get("path"),
                   "d_index" : d_index,
                   "d_generated" : {}}

    return output_data