import logging
from Mixins.mixin_constants import LLM_API_URL, LLM_USER, LLM_PASS
import httpx
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
)


class LLMResponseMixin:
    """
    A mixin class to handle interactions with the LLM API using HTTPX client.

    """

    def get_llm_response(self, prompt: str) -> Any:
        """
        Sends a request to the LLM API and retrieves the response.

        Args:
            prompt (str): The input prompt for the LLM API.

        Returns:
            Any: The response from the LLM API if successful.

        Raises:
            httpx.HTTPStatusError: If the server returns an error response.
            httpx.RequestError: If there is a network issue during the request.
        """
        logging.info("Attempting to fetch LLM response for the given prompt.")

        try:
            with httpx.Client(auth=(LLM_USER, LLM_PASS), timeout=6000) as client:
                response = client.post(url=LLM_API_URL,
                                       json={"prompt": prompt, "app_name": "Sales_Agent"})
                response.raise_for_status()
                logging.info("Successfully fetched response from LLM API.")
                return response.json()

        except httpx.HTTPStatusError as http_err:
            logging.error(
                f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.text}")
            raise

        except httpx.RequestError as req_err:
            logging.error(f"Request error occurred: {req_err}")
            raise

        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            raise
