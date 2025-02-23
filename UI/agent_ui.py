import streamlit as st
import base64
import httpx
import logging

st.set_page_config(page_title="SDR Agent", layout="wide",
                   page_icon="🤑")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


css_file_path = "main.css"
try:
    with open(css_file_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("CSS file not found.")
    logging.error("CSS file not found: %s", css_file_path)
except Exception as e:
    st.error(f"Error loading CSS: {e}")
    logging.error("Error loading CSS: %s", e)


def send_payload(api_url: str, user_query: str):

    auth = ("agent1api", "agent@111")

    payload = {
        "query": str(user_query)
    }

    try:
        with httpx.Client(timeout=3000, auth=auth) as client:
            response = client.post(api_url, json=payload)
            response.raise_for_status()
            logging.info("Successfully sent Payload to API.")
            return response.json()
    except httpx.RequestError as e:
        st.error(f"Network error occurred: {e}")
        logging.error("Network error occurred: %s", e)
    except httpx.HTTPStatusError as e:
        st.error(f"API responded with error: {e}")
        logging.error("API responded with error: %s", e)
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        logging.error("Unexpected error: %s", e)
    return None


# Streamlit UI
st.title("AI Agent | Sales Developement Representative")

user_query = st.text_area("Input Query", height=200)


if st.button("Submit"):
    with st.spinner("Processing...") as spinner:
        if len(user_query) < 3:
            st.error("Please enter a valid query.")
            logging.error("Invalid query length: %s", user_query)
        else:
            API_URL = "http://0.0.0.0:8301/agent/inference/get-response"
            response = send_payload(
                api_url=API_URL, user_query=user_query)

            if response:
                st.subheader("Response:")
                email = response.get("query_response")
                with st.expander(f"Response Body {response['process_time']}s"):
                    st.json(response)
                st.markdown(response['query_response'])