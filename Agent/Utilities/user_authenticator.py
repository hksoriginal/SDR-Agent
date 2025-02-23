import secrets
import logging
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Depends, HTTPException, status

from Constants.user_auth import VALID_USERNAME, VALID_PASSWORD

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s - %(filename)s",
)


security = HTTPBasic()


class UserAuthenticator:
    """
    A class to handle basic HTTP authentication for the FastAPI application.
    Compares provided credentials against predefined valid username and password.
    """

    @staticmethod
    def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
        """
        Verifies the current user based on provided HTTP basic authentication credentials.

        Parameters:
        -----------
        credentials : HTTPBasicCredentials
            The credentials provided by the client (username and password).

        Returns:
        --------
        str:
            The username of the authenticated user if credentials are valid.

        Raises:
        -------
        HTTPException:
            If the username or password is incorrect, raises a 401 Unauthorized error.
        """
        try:
            logging.info("Authenticating user...")

            correct_username = secrets.compare_digest(
                credentials.username, VALID_USERNAME
            )
            correct_password = secrets.compare_digest(
                credentials.password, VALID_PASSWORD
            )

            if not (correct_username and correct_password):
                logging.warning(
                    f"Invalid login attempt with username: {credentials.username}"
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                    headers={"WWW-Authenticate": "Basic"},
                )

            logging.info(f"User '{credentials.username}' authenticated successfully.")
            return credentials.username

        except HTTPException as http_exc:
            logging.error(f"Authentication failed: {http_exc.detail}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during authentication: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during authentication",
            ) from e
