import logging
import torch
import gc
from ctransformers import AutoModelForCausalLM

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class LLMResponse:
    """
    A class for generating responses from a causal language model using ctransformers.
    """

    def __init__(self, model_path: str) -> None:
        """
        Initializes the LLMResponse object with the given parameters.

        Args:
            model_path (str): Path to the pretrained model.
        """
        self.model_path = model_path
        self.llm = self._initialize_model()

    def _initialize_model(self):
        """
        Initializes the language model.

        Returns:
            AutoModelForCausalLM: Loaded language model.
        """
        if not torch.cuda.is_available():
            raise RuntimeError(
                "GPU not available. This code must run on a GPU.")

        try:
            logging.info(
                "Initializing the language model from %s", self.model_path)
            with torch.no_grad():
                model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    model_type="mistral",
                    gpu_layers=-1,
                    max_new_tokens=512,
                    temperature=0.001,
                    top_k=50,
                    top_p=0.9,
                    repetition_penalty=1.2,
                    context_length=2048,
                    threads=-1,
                    stream=False
                )
                logging.info("Model initialized successfully on GPU.")
                return model
        except Exception as e:
            logging.error("Failed to initialize the model: %s", str(e))
            raise

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response based on the given prompt.

        Args:
            prompt (str): Input prompt for the language model.

        Returns:
            str: Generated response.
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            logging.info("Generating response for the prompt.")
            response = self.llm(prompt)
            torch.cuda.empty_cache()
            gc.collect()
            logging.info("Response generated successfully.")
            return response
        except Exception as e:
            logging.error("Error during response generation: %s", str(e))
            raise
