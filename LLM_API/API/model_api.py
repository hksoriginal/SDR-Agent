import json
import logging
import time
import uuid
from datetime import datetime

from typing_extensions import Annotated

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from Utilities.get_llm_response import LLMResponse
from Utilities.user_authenticator import UserAuthenticator
from Constants.api_constants import REQ_PER_MIN

from Handlers.error_handler import ErrorHandlers
from Handlers.json_response_handler import JSONResponseHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
)

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(
        status_code=429, content={"detail": "rate limit exceeded"}
    ),
)

app.add_middleware(SlowAPIMiddleware)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = "Model/mistral-7b-instruct-v0.2.Q5_K_S.gguf"

user_auth = UserAuthenticator()
json_response_handler = JSONResponseHandler()
error_handler = ErrorHandlers()
llm_response = LLMResponse(model_path=model_path)


@app.post("/model_s/inference/get-response")
@limiter.limit(f"{REQ_PER_MIN}/minute")
async def get_audio_transcript(
    request: Request, auth_flag: Annotated[bool, Depends(user_auth.get_current_user)]
) -> JSONResponse:

    start_time = time.time()
    logging.info("Inference request received.")

    try:
        data = await request.json()
        prompt = data.get("prompt")
        app_name = data.get("app_name", "TEST_APP")

        incoming_client_ip = request.client.host
        incoming_client_port = request.client.port

        llm_output = llm_response.generate_response(
            prompt=prompt
        )

        end_time = time.time()
        process_time = round(end_time - start_time, 1)

        result_response = {
            "response_id": str(uuid.uuid1()),
            "process_time": process_time,
            "app_name": app_name,
            "datetime": str(datetime.now()),
            "llm_response": str(llm_output),
            "incoming_client_ip": incoming_client_ip,
            "incoming_client_port": incoming_client_port,
        }

        print("LLM output :",  llm_output)

        logging.info(
            f"Response generated successfully in {process_time} seconds.")
        return json_response_handler.get_200_response(response_dict=result_response)

    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
        FileNotFoundError,
        PermissionError,
        AttributeError,
    ) as e:
        logging.error(f"Request error: {e}")
        return error_handler.handle_error(e, status_code=400)
    except Exception as e:
        logging.error(f"Internal server error: {e}", exc_info=True)
        return error_handler.handle_error(e, status_code=500)
