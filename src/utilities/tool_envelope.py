"""
This module contains the ToolEnvelope class, which is used to standardize the IO of tools.
"""

import inspect
from typing import Any, Dict, List, Optional, get_type_hints

class ToolEnvelope:
    """
    This class is used to standardize the IO of tools.
    """
    def __init__(self, tool: Any):
        self.tool = tool
        self.name = tool.__name__
        self.tool_version = tool.__version__
        self.description = inspect.getdoc(tool) or ""
        self.parameters = get_type_hints(tool)
        self.required_parameters = [param for param in self.parameters if self.parameters[param].default is inspect._empty]
        self.optional_parameters = [param for param in self.parameters if self.parameters[param].default is not inspect._empty]
        self.output_type = get_type_hints(tool).get("return", None)
        self.result_status = None
        self.result_message = None
        self.result_data = None
        self.citations = None
        self.artifacts = None

    def execute(self, input: str) -> str:
        """
        Execute the tool with the given input.
        """

        self.call_envelope()
        self.result_envelope()
        self.envelope()
        
    
    
    # ----- Edit Information -----

    # ---------- Tool Result Information ----------

    def set_result_status(self, result: str) -> None:
        """
        Set the result of the tool.
        """
        self.result_status = result

    def set_result_message(self, result_message: str) -> None:
        """
        Set the result message of the tool.
        """
        self.result_message = result_message

    def set_result_data(self, result_data: list[dict]) -> None:
        """
        Set the result data of the tool.
        """
        self.result_data = result_data

    def set_result_citations(self, citations: list[dict]) -> None:
        """
        Set the citation information of the tool.
        """
        self.citations = citations

    def set_result_artifacts(self, artifacts: list[dict]) -> None:
        """
        Set the artifacts of the tool.
        """
        self.artifacts = artifacts

    # ----- Get Information -----

    def get_name(self) -> str:
        """
        Get the name of the tool.
        """
        return self.name

    def get_tool_version(self) -> str:
        """
        Get the version of the tool.
        """
        return self.tool_version

    def get_description(self) -> str:
        """
        Get the description of the tool.
        """ 
        return self.description
    
    def get_parameters(self) -> dict:
        """
        Get the parameters of the tool.
        """
        return self.parameters
    
    def get_required_parameters(self) -> list:
        """
        Get the required parameters of the tool.
        """
        return self.required_parameters
    
    def get_optional_parameters(self) -> list:
        """
        Get the optional parameters of the tool.
        """
        return self.optional_parameters
    
    def get_output_type(self) -> str:
        """
        Get the output type of the tool.
        """
        return self.output_type
    
    # ---------- Tool Result Information ----------

    def get_result_status(self) -> str:
        """
        Get the result status of the tool.
        """
        return self.result_status
    
    def get_result_message(self) -> str:
        """
        Get the result message of the tool.
        """
        return self.result_message
    
    def get_result_data(self) -> list[dict]:
        """
        Get the result data of the tool.
        """
        return self.result_data
    
    def get_result_citations(self) -> list[dict]:
        """
        Get the citation information of the tool.
        """
        return self.citations
    
    def get_result_artifacts(self) -> list[dict]:
        """
        Get the artifacts of the tool.
        """
        return self.artifacts
    
    # ----- Tool Envelopes -----

    def call_envelope(self) -> dict:
        """
        Get the call envelope of the tool.
        """
        self.call_envelope = {
            "name": self.name,
            "version": self.tool_version,
            "description": self.description,
            "parameters": self.parameters,
            "required_parameters": self.required_parameters,
            "optional_parameters": self.optional_parameters,
            "output_type": self.output_type,
        }
    
    def result_envelope(self) -> dict:
        """
        Get the result envelope of the tool.
        """
        self.result_envelope = {
            "status": self.result_status,
            "message": self.result_message,
            "data": self.result_data,
            "citations": self.citations,
            "artifacts": self.artifacts,
        }
    
    def envelope(self) -> dict:
        """
        Get the envelope of the tool.
        """
        self.envelope = {
            "call": self.call_envelope,
            "result": self.result_envelope,
        }
