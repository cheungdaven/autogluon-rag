import importlib.util
import logging
from typing import Dict

spec = importlib.util.find_spec("vllm")
found = spec is not None

if found:
    from vllm import LLM, SamplingParams

from agrag.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class VLLMGenerator:
    """
    A class used to generate responses based on a query and a given context using the vLLM library.
    Refer to https://docs.vllm.ai/en/latest/ for more information.

    Attributes:
    ----------
    model_name : str
        The name of the vLLM model to use for response generation.
    vllm_init_params : Dict,
        Parameters to initialize vllm, including model configs and vllm engine configs.
        See https://docs.vllm.ai/en/latest/dev/offline_inference/llm.html for more details.
    sampling_params: SamplingParams
        The sampling parameters for vLLM.

    Methods:
    -------
    generate_response(query: str, context: List[str]) -> str:
        Generates a response based on the query and context.
    """

    def __init__(
        self,
        model_name: str,
        vllm_init_params: Dict = None,
        vllm_sampling_params: Dict = None,
    ):
        self.model_name = model_name

        if found:
            self.sampling_params = SamplingParams(**vllm_sampling_params) if vllm_sampling_params else SamplingParams()
            self.llm = LLM(model=self.model_name, **vllm_init_params)

            logger.info(f"Using vLLM Model {self.model_name} for VLLM Generator")
        else:
            logger.warning("vLLM is not supported on this message. Please install vllm.")

    def generate_response(self, query: str) -> str:
        """
        Generates a response based on the query and context.

        Parameters:
        ----------
        query : str
            The user query.

        Returns:
        -------
        str
            The generated response.
        """
        prompts = [query]

        outputs = self.llm.generate(prompts, self.sampling_params)

        generated_text = outputs[0].outputs[0].text
        return generated_text
