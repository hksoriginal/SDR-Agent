from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class JSONResponseHandler:
    """
    A class to handle the creation of JSON responses.

    Methods:
        get_200_response(response_dict: Dict[str, Any]) -> JSONResponse:
            Returns a JSON response with the given content.
    """

    def get_200_response(self, response_dict: Dict[str, Any]) -> JSONResponse:
        """
        Creates a JSON response with a 200 OK status.

        Args:
            response_dict (Dict[str, Any]): The dictionary containing the response data.

        Returns:
            JSONResponse: A FastAPI JSON response object with status code 200.

        Raises:
            ValueError: If the response_dict is not a dictionary.
            Exception: For any other unexpected errors.
        """
        try:
            if not isinstance(response_dict, dict):
                raise ValueError("response_dict must be of type Dict[str, Any].")

            logging.info("Creating a 200 OK JSON response.")
            return JSONResponse(content=response_dict, status_code=200)

        except ValueError as ve:
            logging.error("ValueError encountered: %s", ve)
            raise
        except Exception as e:
            logging.exception(
                "An unexpected error occurred while creating JSON response."
            )
            raise
