import logging
import pandas as pd
from Constants.Agents.dataframe_agent_constants import DATAFRAME_AGENT_PROMPT_TEMPLATE
from Mixins.llm_response_mixin import LLMResponseMixin
from typing import Dict, Any
import re
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataFrameAgent(LLMResponseMixin):
    """
    A class to interact with a filtered DataFrame and extract relevant information
    using LLM responses for dynamic filtering based on user queries.

    Attributes:
        filtered_dataframe (pd.DataFrame): The DataFrame to be filtered.
    """

    def __init__(self):
        """
        Initializes the DataFrameAgent with a filtered DataFrame.
        """
        self.filtered_dataframe = pd.read_csv("./DataFiles/filtred.csv")

    def _extract_json(self, response: str) -> Dict[str, Any]:
        """
        Extracts a JSON object from a string response.

        Args:
            response (str): The string response potentially containing a JSON object.

        Returns:
            Dict[str, Any]: Extracted JSON object.

        Raises:
            ValueError: If JSON extraction or decoding fails.
        """
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                extracted_json = json.loads(json_str)
                logging.info("Successfully extracted JSON from response.")
                return extracted_json
            except json.JSONDecodeError as e:
                logging.error(f"JSON decoding failed: {e}")
                raise ValueError(
                    "Failed to decode JSON from the response.") from e
        else:
            logging.warning("No JSON object found in the response.")
            raise ValueError("No JSON object found in the response.")

    def get_filter_params(self, action: str) -> Dict[str, str]:
        """
        Generates filtering parameters using the LLM based on a user-defined action.

        Args:
            action (str): The action/query describing how to filter the data.

        Returns:
            Dict[str, str]: A dictionary containing filtering parameters like column and condition.
        """
        try:
            prompt = DATAFRAME_AGENT_PROMPT_TEMPLATE.format(data_query=action)
            response = self.get_llm_response(prompt=prompt)
            extracted_json = self._extract_json(
                response=response['llm_response'])
            return extracted_json
        except KeyError as e:
            logging.error(
                f"KeyError encountered while extracting LLM response: {e}")
            return {"error": "Failed to process the action due to missing response data."}
        except Exception as e:
            logging.exception(f"Unexpected error occurred: {e}")
            return {"error": "An unexpected error occurred while processing the action."}

    def get_filtred_data(self, action: str) -> str:
        """
        Filters the DataFrame based on parameters extracted from the LLM response.

        Args:
            action (str): The user-defined action/query for filtering the data.

        Returns:
            str: A JSON string of the filtered DataFrame.
        """
        try:
            params = self.get_filter_params(action=action)
            if "error" in params:
                return json.dumps(params)

            column = params.get("column", "")
            condition = params.get("condition", "")

            if column not in self.filtered_dataframe.columns:
                logging.error(f"Invalid column name provided: {column}")
                return json.dumps({"error": "Invalid column name."})

            new_df = self.filtered_dataframe[
                self.filtered_dataframe[column].astype(
                    str).str.contains(condition.lower(), case=False, na=False)
            ]

            logging.info(
                f"Data successfully filtered based on column '{column}' and condition '{condition}'.")
            return new_df.to_json()
        except Exception as e:
            logging.exception(f"Error occurred while filtering data: {e}")
            return json.dumps({"error": "An unexpected error occurred while filtering data."})
