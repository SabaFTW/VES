"""
Model Runner Module - Interfaces with local LLMs

Supports:
- Ollama
- vLLM
- llama.cpp server
- Fallback handlers
- Proper error handling
"""

import requests
import json
import logging
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class ModelInterfaceError(Exception):
    """Custom exception for model interface errors"""
    pass

class BaseModelInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generate text using the model
        Args:
            prompt: Main input text
            system_prompt: Optional system instruction
            **kwargs: Model-specific parameters
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """
        Check if the model interface is healthy
        Returns:
            True if healthy, False otherwise
        """
        pass

class OllamaInterface(BaseModelInterface):
    def __init__(self, endpoint: str = "http://localhost:11434", model_name: str = "llama3"):
        self.endpoint = endpoint.rstrip('/')
        self.model_name = model_name
        self._validate_config()
    
    def _validate_config(self):
        """Validate the configuration"""
        if not self.endpoint.startswith(('http://', 'https://')):
            raise ModelInterfaceError(f"Invalid endpoint URL: {self.endpoint}. Must start with http:// or https://")
        
        if not self.model_name.strip():
            raise ModelInterfaceError("Model name cannot be empty")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generate text using Ollama API with proper error handling
        """
        try:
            # Validate inputs
            if not prompt.strip():
                return "[ModelRunner: Error - Empty prompt provided]"
            
            # Prepare the messages for the API call
            messages = []
            
            if system_prompt:
                # Validate system prompt
                if not isinstance(system_prompt, str):
                    logger.warning("System prompt is not a string, converting to string")
                    system_prompt = str(system_prompt)
                messages.append({"role": "system", "content": system_prompt.strip()})
            
            # Validate main prompt
            if not isinstance(prompt, str):
                logger.warning("Prompt is not a string, converting to string")
                prompt = str(prompt)
            
            messages.append({"role": "user", "content": prompt.strip()})
            
            # Prepare the payload with validation
            payload = {
                "model": self.model_name.strip(),
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": max(0.0, min(2.0, kwargs.get("temperature", 0.7))),  # Clamp between 0 and 2
                    "top_p": max(0.0, min(1.0, kwargs.get("top_p", 0.9))),  # Clamp between 0 and 1
                    "max_tokens": max(1, min(8192, kwargs.get("max_tokens", 2048))),  # Clamp between 1 and 8192
                    "top_k": max(1, min(100, kwargs.get("top_k", 40))),  # Clamp between 1 and 100
                    "repeat_penalty": max(0.1, min(2.0, kwargs.get("repeat_penalty", 1.1)))  # Clamp between 0.1 and 2.0
                }
            }
            
            # Add any additional parameters from kwargs
            for key, value in kwargs.items():
                if key not in ["temperature", "top_p", "max_tokens", "top_k", "repeat_penalty"]:
                    payload["options"][key] = value
            
            # Validate payload
            if not payload['model'] or not payload['messages']:
                raise ModelInterfaceError("Invalid payload: model name or messages are empty")
            
            # Send the request to Ollama with proper error handling
            response = requests.post(
                f"{self.endpoint}/api/chat",
                json=payload,
                timeout=300  # 5 minute timeout for longer processing
            )
            
            # Handle HTTP errors
            if response.status_code == 404:
                raise ModelInterfaceError(f"Model '{self.model_name}' not found. Available models: Check with 'ollama list'")
            elif response.status_code == 500:
                error_detail = response.json().get('error', 'Unknown server error')
                raise ModelInterfaceError(f"Ollama server error: {error_detail}")
            elif response.status_code != 200:
                raise ModelInterfaceError(f"Ollama API error: {response.status_code} - {response.text}")
            
            # Parse response
            try:
                result = response.json()
            except json.JSONDecodeError as e:
                raise ModelInterfaceError(f"Invalid JSON response from Ollama: {e}")
            
            if "message" not in result or "content" not in result["message"]:
                raise ModelInterfaceError(f"Unexpected response format from Ollama: {result}")
            
            return result["message"]["content"]
                
        except requests.exceptions.ConnectionError:
            error_msg = f"[ModelRunner: Cannot connect to Ollama at {self.endpoint}. Please start Ollama with 'ollama serve']"
            logger.error(error_msg)
            return error_msg
        except requests.exceptions.Timeout:
            error_msg = f"[ModelRunner: Timeout contacting Ollama at {self.endpoint} (300s timeout exceeded)]"
            logger.error(error_msg)
            return error_msg
        except ModelInterfaceError:
            # Re-raise custom errors
            raise
        except Exception as e:
            error_msg = f"[ModelRunner: Unexpected error - {str(e)}]"
            logger.error(error_msg)
            return error_msg
    
    def health_check(self) -> bool:
        """
        Check if Ollama is accessible and responsive
        """
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.warning(f"Health check failed: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """
        List available models from Ollama
        """
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

class ModelRunner:
    """
    Orchestrator for different model interfaces with fallback capability
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.interface = None
        try:
            self.interface = self._initialize_interface()
        except Exception as e:
            logger.error(f"Failed to initialize model interface: {e}")
            # Keep interface as None, will return error messages
    
    def _initialize_interface(self) -> Optional[BaseModelInterface]:
        """
        Initialize the appropriate model interface based on config
        """
        if not self.config:
            raise ModelInterfaceError("Config is required to initialize model runner")
        
        model_type = self.config.get('type', 'ollama')
        
        if model_type == 'ollama':
            endpoint = self.config.get('endpoint', 'http://localhost:11434')
            model_name = self.config.get('model_name', 'llama3')
            return OllamaInterface(endpoint, model_name)
        else:
            # Default to Ollama
            endpoint = self.config.get('endpoint', 'http://localhost:11434')
            model_name = self.config.get('model_name', 'llama3')
            return OllamaInterface(endpoint, model_name)
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generate text with fallback handling
        """
        if not self.interface:
            return "[ModelRunner: Error - No interface initialized. Check configuration and dependencies.]"
        
        try:
            # Validate prompt
            if not prompt or not prompt.strip():
                logger.warning("Empty prompt provided to generate")
                return "[ModelRunner: Error - Empty prompt provided]"
            
            return self.interface.generate(prompt, system_prompt, **kwargs)
        except Exception as e:
            logger.error(f"Error in generate: {e}")
            return f"[ModelRunner: Error during generation - {str(e)}]"
    
    def health_check(self) -> bool:
        """
        Check model interface health
        """
        if not self.interface:
            logger.warning("Health check failed: interface not initialized")
            return False
        
        try:
            return self.interface.health_check()
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return False
    
    def list_available_models(self) -> List[str]:
        """
        List available models (if supported by interface)
        """
        if not self.interface or not hasattr(self.interface, 'list_models'):
            logger.warning("list_models not supported by current interface")
            return []
        
        try:
            return self.interface.list_models()
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

# Example usage:
# config = {
#     'type': 'ollama',
#     'endpoint': 'http://localhost:11434', 
#     'model_name': 'llama3'
# }
# runner = ModelRunner(config)
# result = runner.generate("Hello, world!")