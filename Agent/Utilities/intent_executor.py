import logging
from typing import Dict
from Agents.dataframe_agent import DataFrameAgent
from Agents.email_agent import EmailAgent

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class IntentExecutor:
    """
    Executes specific actions based on the provided intent.

    Methods:
        select_and_execute_agent_from_intent(intent_body):
            Executes the corresponding action based on the intent provided in the dictionary.
    """

    def select_and_execute_agent_from_intent(self, intent_body: Dict[str, str]) -> str:
        """
        Selects and executes an agent action based on the given intent.

        Args:
            intent_body (Dict[str, str]): A dictionary containing 'intent' and 'action'.

        Returns:
            str: The response from the executed agent action.

        Raises:
            ValueError: If the intent is not recognized or the action is invalid.
        """
        INTENT_MAP = {
            "write_email": EmailAgent().generate_email,
            "search_dataframe": DataFrameAgent().get_filtred_data
        }

        try:
            intent = intent_body.get('intent')
            action = intent_body.get('action')

            if not intent or not action:
                raise ValueError(
                    "Intent body must contain both 'intent' and 'action' keys.")

            if intent not in INTENT_MAP:
                raise ValueError(f"Unknown intent: {intent}")

            logging.info(f"Executing intent: {intent} with action: {action}")
            response_based_on_intent = INTENT_MAP[intent](action=action)
            logging.info(f"Response from {intent}: {response_based_on_intent}")

            return response_based_on_intent

        except Exception as e:
            logging.error(f"Error executing intent: {e}")
            raise
