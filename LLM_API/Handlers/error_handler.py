import logging
from fastapi.responses import JSONResponse
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class ErrorHandlers:
    def handle_error(self, exception: Exception, status_code: int) -> JSONResponse:
        """
        A helper function to handle logging and responding with appropriate error messages.

        Args:
            exception (Exception): The exception instance.
            status_code (int): HTTP status code to return in the response.

        Returns:
            JSONResponse: The formatted JSON response.
        """
        error_message = str(exception)

        if isinstance(exception, json.JSONDecodeError):
            return self.handle_json_decode_error(error_message)
        elif isinstance(exception, KeyError):
            return self.handle_key_error(error_message)
        elif isinstance(exception, TypeError):
            return self.handle_type_error(error_message)
        elif isinstance(exception, ValueError):
            return self.handle_value_error(error_message)
        elif isinstance(exception, FileNotFoundError):
            return self.handle_file_not_found_error(error_message)
        elif isinstance(exception, PermissionError):
            return self.handle_permission_error(error_message)
        elif isinstance(exception, AttributeError):
            return self.handle_attribute_error(error_message)
        else:
            return self.handle_unexpected_error(error_message, status_code)

    def handle_json_decode_error(self, error_message: str) -> JSONResponse:
        logger.error(f"Invalid JSON format: {error_message}")
        response_content = {"error": "Invalid JSON format in request body"}
        return JSONResponse(content=response_content, status_code=400)

    def handle_key_error(self, error_message: str) -> JSONResponse:
        logger.error(f"Missing key: {error_message}")
        response_content = {"error": f"Missing key: {error_message}"}
        return JSONResponse(content=response_content, status_code=400)

    def handle_type_error(self, error_message: str) -> JSONResponse:
        logger.error(f"TypeError encountered: {error_message}")
        response_content = {
            "error": f"An error occurred due to a type mismatch: {error_message}"
        }
        return JSONResponse(content=response_content, status_code=400)

    def handle_value_error(self, error_message: str) -> JSONResponse:
        logger.error(f"ValueError encountered: {error_message}")
        response_content = {"error": f"Invalid value encountered: {error_message}"}
        return JSONResponse(content=response_content, status_code=400)

    def handle_file_not_found_error(self, error_message: str) -> JSONResponse:
        logger.error(f"FileNotFoundError: {error_message}")
        response_content = {"error": "File not found"}
        return JSONResponse(content=response_content, status_code=404)

    def handle_permission_error(self, error_message: str) -> JSONResponse:
        logger.error(f"PermissionError: {error_message}")
        response_content = {"error": "Permission denied"}
        return JSONResponse(content=response_content, status_code=403)

    def handle_attribute_error(self, error_message: str) -> JSONResponse:
        logger.error(f"AttributeError: {error_message}")
        response_content = {"error": "Invalid attribute access"}
        return JSONResponse(content=response_content, status_code=400)

    def handle_unexpected_error(
        self, error_message: str, status_code: int
    ) -> JSONResponse:
        logger.exception(f"An unexpected error occurred: {error_message}")
        response_content = {"error": "An unexpected error occurred"}
        return JSONResponse(content=response_content, status_code=status_code)
