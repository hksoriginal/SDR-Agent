import re
import json
from typing import Dict
from Constants.api_constants import APP_NAME
from Constants.prompt_templated import INTENT_DETECTION_PROMPT_TEMPLATE
from Mixins.llm_response_mixin import LLMResponseMixin


class IntentDetection(LLMResponseMixin):

    def get_intent(self, query: str) -> Dict[str, str]:
        prompt = INTENT_DETECTION_PROMPT_TEMPLATE.format(query=query)
        response = self.get_llm_response(prompt=prompt)
        extracted_json = self._extract_json(response=response['llm_response'])

        return extracted_json

    def _extract_json(self, response: str) -> Dict[str, str]:
        match = re.search(r'\{.*\}', response, re.DOTALL)

        if match:
            json_str = match.group(0)
            try:
                extracted_json = json.loads(json_str)
                return extracted_json
            except json.JSONDecodeError as e:
                raise
