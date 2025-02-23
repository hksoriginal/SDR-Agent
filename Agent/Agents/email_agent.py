import logging
from Constants.Agents.email_agent_constants import EMAIL_PROMPT_TEMPLATE
from Mixins.llm_response_mixin import LLMResponseMixin
from typing import Dict
import re
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailAgent(LLMResponseMixin):
    """
    EmailAgent class for generating sales emails using a language model.
    Inherits from LLMResponseMixin to utilize LLM response generation.
    """

    def _extract_json(self, response: str) -> Dict[str, str]:
        match = re.search(r'\{.*\}', response, re.DOTALL)

        if match:
            json_str = match.group(0)
            try:
                extracted_json = json.loads(json_str)
                return extracted_json
            except json.JSONDecodeError as e:
                raise

    def generate_email(self, action: str):
        """
        Generates a personalized sales email.
        Returns:
            str: Generated sales email content.
        """
        try:
            prompt = EMAIL_PROMPT_TEMPLATE.format(email_query=action)
            response = self.get_llm_response(prompt=prompt)
            extracted_json = self._extract_json(
                response=response['llm_response'])
            print(extracted_json)
            return extracted_json
        except KeyError as e:
            logger.error(f"KeyError encountered: {e}")
            return "An error occurred while generating the email response."
        except Exception as e:
            logger.exception(f"Unexpected error occurred: {e}")
            return "An unexpected error occurred while generating the email."
