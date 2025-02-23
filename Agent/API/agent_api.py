import json
import logging
import time
import torch
import uuid
import gc
from datetime import datetime

from typing_extensions import Annotated

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from Utilities.data_processor import DataProcessor
from Utilities.intent_executor import IntentExecutor
from Utilities.intent_detection import IntentDetection
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


intent_detection = IntentDetection()
intent_executor = IntentExecutor()
user_auth = UserAuthenticator()
json_response_handler = JSONResponseHandler()
error_handler = ErrorHandlers()
data_processor = DataProcessor(df1_path="./DataFiles/Leads.csv",
                               df2_path="./DataFiles/SampleData.csv")

filtered_dataframe = data_processor.get_filter_data()
data_processor.save_filtered_dataframe(
    filtered_dataframe=filtered_dataframe, path="./DataFiles/filtered.csv")


@app.post("/agent/inference/get-response")
@limiter.limit(f"{REQ_PER_MIN}/minute")
async def get_audio_transcript(
    request: Request, auth_flag: Annotated[bool, Depends(user_auth.get_current_user)]
) -> JSONResponse:

    start_time = time.time()
    logging.info("Inference request received.")

    try:
        data = await request.json()
        query = data.get("query")

        incoming_client_ip = request.client.host
        incoming_client_port = request.client.port

        intent_body = intent_detection.get_intent(query=query)

        intent_response = intent_executor.select_and_execute_agent_from_intent(
            intent_body=intent_body)

        end_time = time.time()
        process_time = round(end_time - start_time, 1)

<<<<<<< HEAD
        torch.cuda.clear_cache()
=======
        torch.cuda.empty_cache()
>>>>>>> f6f648b (new commit)
        gc.collect()

        result_response = {
            "response_id": str(uuid.uuid1()),
            "datetime": str(datetime.now()),
            "intent": intent_body,
            "query_response": intent_response,
            "process_time": process_time,
            "incoming_client_ip": incoming_client_ip,
            "incoming_client_port": incoming_client_port,
        }

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
