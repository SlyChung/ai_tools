"""
Tools for working with APIs.
"""

from library.logger import ScribeLogger
import os
from dotenv import load_dotenv
import openai
import anthropic
from tools import file_management as fm
from llama_cpp import Llama
import tiktoken
import json
from library.config import PROJECT_ROOT

error_logger = ScribeLogger("error")
api_logger = ScribeLogger("api")
technical_logger = ScribeLogger("technical")


# Load environment variables
load_dotenv()


# Configure API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")



def query_openai(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.5, system_prompt: str = None, max_output_tokens: int = 200) -> str:
    """
    Query the OpenAI API.
    """

    input_tokens = gpt_token_count(f"{system_prompt}\n\n{prompt}", model)
    context_window = get_context_window(model)
    max_output_tokens = get_max_output_tokens(model)

    if input_tokens < context_window:
        if system_prompt:
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        else:
            messages=[
                {"role": "user", "content": prompt}
            ]
    else:
        error_logger.log_error(f"llm.query_openai: Too many input tokens for model {model}")
        return None

    api_logger.log_info(f"llm.query_openai: Querying OpenAI API to model {model}")
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_output_tokens,
    )
    return response.choices[0].message.content

# Does not work.
def query_anthropic(prompt: str, model: str = "claude-3-5-sonnet-20240620", temperature: float = 0.5, system_prompt: str = None) -> str:
    """
    Query the Anthropic API.
    """
    
    api_logger.log_info(f"Querying Anthropic API to model {model}")
    response = anthropic.messages.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def query_local_llm(prompt: str, model: str = "mistral-7b-instruct-v0.1.Q8_0.gguf", temperature: float = 0.5, system_prompt: str = None, max_tokens: int = 200) -> str:
    """
    Query the local LLM.
    """
    input_tokens = local_token_count(f"{system_prompt}\n\n{prompt}", model)
    max_output_tokens = get_max_output_tokens(model)
    context_window = get_context_window(model)
    if input_tokens > context_window:
        error_logger.log_error(f"llm.query_local_llm: Too many input tokens for model {model}")
        return None
    
    prompt = f"{system_prompt}\n\n{prompt}"

    api_logger.log_info(f"Querying local LLM to model {model}")
    llm = Llama(
        model_path=f"{PROJECT_ROOT}/models/{model}",
        n_ctx=max_output_tokens,
        n_gpu_layers=-1,
        verbose=False
    )
    return llm(prompt, max_tokens=max_tokens,temperature=temperature, stop=["</s>"])

def get_local_models() -> list[str]:
    """
    Get a list of all Available Local Models.

    returns:
        list of model names
    """
    technical_logger.log_info("Getting local models")
    return fm.list_files(f"{PROJECT_ROOT}/models/local") 

def local_token_count(prompt: str, model: str = "mistral-7b-instruct-v0.1.Q8_0.gguf") -> int:
    """
    Get the number of tokens from a local model in the prompt.
    """
    technical_logger.log_info(f"llm.local_token_count: Getting token count for local model {model}")
    llm = Llama(
        model_path=f"{PROJECT_ROOT}/models/{model}",
        n_ctx=8192,
        n_gpu_layers=-1,
        verbose=False
    )
    return llm.token_count(prompt)

def gpt_token_count(prompt: str, model: str = "gpt-4o-mini") -> int:
    """
    Get the number of tokens from a gpt model in the prompt.
    """
    technical_logger.log_info(f"llm.gpt_token_count: Getting token count for gpt model {model}")
    encoding = tiktoken.encoding_for_model(model)
    #technical_logger.log_info(f"llm.gpt_token_count: Encoding prompt for gpt model {model}")
    tokens = encoding.encode(prompt)
    #technical_logger.log_info(f"llm.gpt_token_count: Token count for gpt model {model} is {len(tokens)}")
    return len(tokens)

# Does not work.
def claude_token_count(prompt: str, model: str = "claude-3-5-sonnet-20240620") -> int:
    """
    Get the number of tokens from a claude model in the prompt.

    Does not work.
    """
    technical_logger.log_info(f"llm.claude_token_count: Getting token count for claude model {model}")
    return 100000

def get_context_window(model: str) -> int:
    """
    Get the context window for a model.
    """
    technical_logger.log_info(f"llm.get_context_window: Getting context window for model {model}")
    model_registry = fm.read_file(f"{PROJECT_ROOT}/models", "model_registry.json")
    model_registry = json.loads(model_registry)
    model_info = model_registry.get(model)
    return model_info.get("context_window")

def get_max_output_tokens(model: str) -> int:
    """
    Get the max output tokens for a model.
    """
    technical_logger.log_info(f"llm.get_max_output_tokens: Getting max output tokens for model {model}")
    model_registry = fm.read_file(f"{PROJECT_ROOT}/models", "model_registry.json")
    model_registry = json.loads(model_registry)
    model_info = model_registry.get(model)
    return model_info.get("max_output_tokens")

def query_llm(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.5, system_prompt: str = None) -> str:
    """
    Query the LLM.
    """
    # Get the model info from the model registry.
    technical_logger.log_info(f"llm.query_llm: Getting model info for model {model}")
    model_registry = fm.read_file(f"{PROJECT_ROOT}/models", "model_registry.json")
    model_registry = json.loads(model_registry)
    model_info = model_registry.get(model)

    if model_info is None:
        error_logger.log_error(f"llm.query_llm: Model {model} not found in model registry")
        return None

    """
    Get the number of tokens from the prompt and subtract it from the token window.
    Then query the LLM with the remaining tokens.
    """

    # Query the LLM based on the provider.
    if model_info.get("provider") == "openai":
        return query_openai(prompt, model, temperature, system_prompt, model_info.get("max_output_tokens"))
    # Does not work.
    elif model_info.get("provider") == "anthropic":
        return query_anthropic(prompt, model, temperature, system_prompt)
    elif model_info.get("provider") == "local":
        return query_local_llm(prompt, model, temperature, system_prompt, model_info.get("max_output_tokens"))
    
def pick_model() -> str:
    """
    Placeholder for smart model selection.
    """
    technical_logger.log_info("llm.pick_model: Picking model")
    return "gpt-3.5-turbo"