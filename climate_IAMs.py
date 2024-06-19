import numpy as np
import pandas as pd
from openai import OpenAI
import json



def get_climate_change(variable, year, scenario):
    """Get the climate related variables data in given year and scenario."""
    df = pd.read_csv('magicc7_res_World_CI_2024_2100.csv')
    col = ['model','quantile', 'variable','unit', 'scenario', year]
    return df[col][(df['variable'] == variable) & (df['scenario'] == scenario)].to_json()

def get_chatiams(messages):
    openai_client = OpenAI(api_key="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")
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_climate_change",
                "description": "Get the climate change data in a given variables, year, scenario and region ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "variable": {
                            "type": "string",
                            "description": "a range of climate-related metrics",
                            "enum": ["Surface Air Temperature Change",
                            "Atmospheric Concentrations|CO2",
                            "Effective Radiative Forcing",
                            "Effective Radiative Forcing|CO2",
                            "Effective Radiative Forcing|Aerosols",
                            "Effective Radiative Forcing|Aerosols|Direct Effect|BC",
                            "Effective Radiative Forcing|Aerosols|Direct Effect|OC",
                            "Effective Radiative Forcing|Aerosols|Direct Effect|SOx",
                            "Effective Radiative Forcing|Aerosols|Direct Effect",
                            "Effective Radiative Forcing|Aerosols|Indirect Effect",
                            "Sea Level Change"]
                        },
                        "year": {"type": "string", "description": "years starting from 2024 to 2100"},
                        "scenario": {
                            "type": "string",
                            "description": "a list of climate scenario settings",
                            "enum": ['ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp460', 'ssp585']
                        },
                    },
                    "required": ["variable", "year", "scenario"],
                },
            },
        }
    ]
    # messages = [{"role": "user", "content": question}]
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # Step 2: check if the model wanted to call a function

    if tool_calls:
        # messages = [{"role": "user", "content": question}]
        # messages = [
        # {"role": "system", "content": 'You are a helpful climate assistant. You will answer the question about temperature change and sea level change.'},
        # {"role": "user", "content": question}
        # ]
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_climate_change": get_climate_change
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                variable=function_args.get("variable"),
                year=function_args.get("year"),
                scenario = function_args.get("scenario"),
                # temperature = function_args.get("temperature")
                # value = function_args.get("value")
            )
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        
        second_response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )  # get a new response from the model where it can see the function response
    else:
        second_response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
    return second_response


# question = "What is the World Surface Air Temperature Change under ssp245 in 2033?"
# print(get_chatiams(question))