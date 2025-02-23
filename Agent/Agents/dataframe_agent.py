import logging
import pandas as pd
from Constants.Agents.dataframe_agent_constants import DATAFRAME_AGENT_PROMPT_TEMPLATE
from Mixins.llm_response_mixin import LLMResponseMixin
from typing import Dict
import re
import json


logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataFrameAgent(LLMResponseMixin):

    def __init__(self):
        self.filtered_dataframe = pd.read_csv('./DataFiles/filtered.csv')

    def _extract_json(self, response: str) -> Dict[str, str]:
        match = re.search(r'\{.*\}', response, re.DOTALL)

        if match:
            json_str = match.group(0)
            try:
                extracted_json = json.loads(json_str)
                return extracted_json
            except json.JSONDecodeError as e:
                raise

    def get_filter_params(self, action: str):
        try:
            prompt = DATAFRAME_AGENT_PROMPT_TEMPLATE.format(
                data_query=action)
            response = self.get_llm_response(prompt=prompt)
            extracted_json = self._extract_json(
                response=response['llm_response'])
            return extracted_json
        except KeyError as e:
            logging.error(f"KeyError encountered: {e}")
            return "An error occurred while generating the email response."
        except Exception as e:
            logging.exception(f"Unexpected error occurred: {e}")
            return "An unexpected error occurred while generating the email."

    def get_filtred_data(self, action: str):

        params = self.get_filter_params(action=action)
        column = params.get("column", "")
        condition = params.get("condition", "")

        new_df = self.filtered_dataframe[self.filtered_dataframe[column].str.contains(
            condition, case=False, na=False)]

        return new_df.to_json()
