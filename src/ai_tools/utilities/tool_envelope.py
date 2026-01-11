"""
Standardized wrapper for tool input/output handling.

This module provides the ToolEnvelope class, which wraps callable tools
to provide consistent metadata extraction, execution, and result formatting.
All tool calls produce a standardized envelope containing call metadata
and result data.

Example:
    from ai_tools.utilities.tool_envelope import ToolEnvelope

    @version("1.0.0")
    def my_tool(param1: str) -> dict:
        return {"status": True, "data": {"result": param1}}

    envelope = ToolEnvelope(my_tool)
    result = envelope.execute({"param1": "value"})
    # result contains {"call": {...}, "result": {...}}
"""

import inspect
from typing import Any, Dict, List, Optional, get_type_hints


class ToolEnvelope:
    """Wrapper that standardizes tool execution and result formatting.

    Extracts metadata from a callable (name, version, parameters, types)
    and provides a consistent interface for execution and result access.

    The envelope format separates call metadata from result data:
    - call: Tool name, version, description, parameters, types
    - result: status, message, data, citations, artifacts

    Attributes:
        tool: The wrapped callable.
        name: Name of the tool function.
        tool_version: Version string from __version__ attribute.
        description: Tool's docstring.
        signature: Function signature object.
        parameters: Dictionary of parameter objects.
        required_parameters: List of required parameter names.
        optional_parameters: List of optional parameter names.
        output_type: Return type annotation.
        result_status: Execution status (True/False/None).
        result_message: Human-readable result message.
        result_data: The actual result data.
        citations: Optional list of citation references.
        artifacts: Optional list of artifacts produced.
    """

    def __init__(self, tool: Any):
        """Initialize a ToolEnvelope with a callable.

        Args:
            tool: A callable (function or method) to wrap. May have a
                __version__ attribute from the @version decorator.
        """
        self.tool = tool
        self.name = tool.__name__
        self.tool_version = getattr(tool, "__version__", "0.0.0")
        self.description = inspect.getdoc(tool) or ""
        self.signature = inspect.signature(tool)
        self.parameters = self.signature.parameters
        self.required_parameters = [
            p for p, obj in self.parameters.items()
            if obj.default is inspect._empty and obj.kind in (obj.POSITIONAL_OR_KEYWORD, obj.KEYWORD_ONLY)
        ]
        self.optional_parameters = [
            p for p, obj in self.parameters.items()
            if obj.default is not inspect._empty and obj.kind in (obj.POSITIONAL_OR_KEYWORD, obj.KEYWORD_ONLY)
        ]
        self.output_type = self.signature.return_annotation

        # result fields
        self.result_status: bool | None = None
        self.result_message: str | None = None
        self.result_data: Any = None
        self.citations: List[Dict[str, Any]] | None = None
        self.artifacts: List[Dict[str, Any]] | None = None

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the wrapped tool and return a standardized envelope.

        Args:
            inputs: Dictionary of parameter names to values to pass to the tool.

        Returns:
            A dictionary with 'call' and 'result' keys containing metadata
            and execution results respectively.
        """
        # build call metadata first
        self._call_envelope = self.call_envelope()


        # run the tool
        result = self.tool(**inputs)


        # map common shapes into fields; fall back gracefully
        if isinstance(result, dict):
            self.result_status = result.get("status")
            self.result_message = result.get("message")
            self.result_data = result.get("data")
            self.citations = result.get("citations")
            self.artifacts = result.get("artifacts")
        else:
            self.result_status = True
            self.result_message = "ok"
            self.result_data = result


        self._result_envelope = self.result_envelope()
        self._envelope = self.envelope()
        return self._envelope
        
    
    
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

    def call_envelope(self) -> Dict[str, Any]:
        """Build the call metadata envelope.

        Returns:
            Dictionary containing tool metadata: name, version, description,
            parameters, required/optional parameters, and output type.
        """
        return {
            "name": self.name,
            "version": self.tool_version,
            "description": self.description,
            "parameters": {
                k: {
                    "kind": str(v.kind),
                    "default": None if v.default is inspect._empty else v.default,
                    "annotation": str(v.annotation) if v.annotation is not inspect._empty else None,
                }
                for k, v in self.parameters.items()
            },
            "required_parameters": self.required_parameters,
            "optional_parameters": self.optional_parameters,
            "output_type": str(self.output_type),
        }
    
    def result_envelope(self) -> Dict[str, Any]:
        """Build the result envelope.

        Returns:
            Dictionary containing execution results: status, message,
            data, citations, and artifacts.
        """
        return {
            "status": self.result_status,
            "message": self.result_message,
            "data": self.result_data,
            "citations": self.citations,
            "artifacts": self.artifacts,
        }

    def envelope(self) -> Dict[str, Any]:
        """Get the complete tool envelope with call and result sections.

        Returns:
            Dictionary with 'call' containing tool metadata and 'result'
            containing execution results. Only valid after execute() is called.
        """
        return {
            "call": self._call_envelope,
            "result": self._result_envelope,
        }
