"""
Tests for ToolEnvelope in src/ai_tools/utilities/tool_envelope.py

Production-ready component - all tests should pass.
"""

import pytest
from typing import Dict, Any
from ai_tools.utilities.tool_envelope import ToolEnvelope


class TestToolEnvelopeInit:
    """Tests for ToolEnvelope initialization."""

    @pytest.mark.production
    def test_init_captures_function_name(self, sample_tool_function):
        """Test that ToolEnvelope captures the function name."""
        envelope = ToolEnvelope(sample_tool_function)
        assert envelope.name == "sample_add"

    @pytest.mark.production
    def test_init_captures_version(self, sample_tool_function):
        """Test that ToolEnvelope captures the function version."""
        envelope = ToolEnvelope(sample_tool_function)
        assert envelope.tool_version == "1.0.0"

    @pytest.mark.production
    def test_init_captures_docstring(self, sample_tool_function):
        """Test that ToolEnvelope captures the function docstring."""
        envelope = ToolEnvelope(sample_tool_function)
        assert "Add two numbers" in envelope.description

    @pytest.mark.production
    def test_init_identifies_required_parameters(self, sample_tool_function):
        """Test that ToolEnvelope identifies required parameters."""
        envelope = ToolEnvelope(sample_tool_function)
        assert "a" in envelope.required_parameters
        assert "b" in envelope.required_parameters
        assert "optional" not in envelope.required_parameters

    @pytest.mark.production
    def test_init_identifies_optional_parameters(self, sample_tool_function):
        """Test that ToolEnvelope identifies optional parameters."""
        envelope = ToolEnvelope(sample_tool_function)
        assert "optional" in envelope.optional_parameters
        assert "a" not in envelope.optional_parameters

    @pytest.mark.production
    def test_init_default_version_when_missing(self):
        """Test that ToolEnvelope uses default version when __version__ is missing."""
        def no_version_func(x: int) -> int:
            """A function without version."""
            return x

        envelope = ToolEnvelope(no_version_func)
        assert envelope.tool_version == "0.0.0"

    @pytest.mark.production
    def test_init_result_fields_are_none(self, sample_tool_function):
        """Test that result fields start as None."""
        envelope = ToolEnvelope(sample_tool_function)
        assert envelope.result_status is None
        assert envelope.result_message is None
        assert envelope.result_data is None
        assert envelope.citations is None
        assert envelope.artifacts is None


class TestToolEnvelopeExecute:
    """Tests for ToolEnvelope.execute() method."""

    @pytest.mark.production
    def test_execute_runs_function(self, sample_tool_function):
        """Test that execute runs the wrapped function."""
        envelope = ToolEnvelope(sample_tool_function)
        result = envelope.execute({"a": 5, "b": 3})

        assert result is not None

    @pytest.mark.production
    def test_execute_extracts_status_from_dict(self, sample_tool_function):
        """Test that execute extracts status from dict result."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.execute({"a": 5, "b": 3})

        assert envelope.result_status is True

    @pytest.mark.production
    def test_execute_extracts_data_from_dict(self, sample_tool_function):
        """Test that execute extracts data from dict result."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.execute({"a": 5, "b": 3})

        assert envelope.result_data == {"result": 8}

    @pytest.mark.production
    def test_execute_extracts_message_from_dict(self, sample_tool_function):
        """Test that execute extracts message from dict result."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.execute({"a": 5, "b": 3})

        assert envelope.result_message == "Addition successful"

    @pytest.mark.production
    def test_execute_handles_non_dict_result(self):
        """Test that execute handles non-dict return values."""
        def simple_func(x: int) -> int:
            return x * 2

        envelope = ToolEnvelope(simple_func)
        envelope.execute({"x": 5})

        assert envelope.result_status is True
        assert envelope.result_message == "ok"
        assert envelope.result_data == 10

    @pytest.mark.production
    def test_execute_with_optional_parameter(self, sample_tool_function):
        """Test execute with optional parameter provided."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.execute({"a": 1, "b": 2, "optional": "custom"})

        assert envelope.result_status is True

    @pytest.mark.production
    def test_execute_extracts_citations(self):
        """Test that execute extracts citations from result."""
        def func_with_citations() -> Dict[str, Any]:
            return {
                "status": True,
                "message": "ok",
                "data": {},
                "citations": [{"source": "test"}]
            }

        envelope = ToolEnvelope(func_with_citations)
        envelope.execute({})

        assert envelope.citations == [{"source": "test"}]

    @pytest.mark.production
    def test_execute_extracts_artifacts(self):
        """Test that execute extracts artifacts from result."""
        def func_with_artifacts() -> Dict[str, Any]:
            return {
                "status": True,
                "message": "ok",
                "data": {},
                "artifacts": [{"name": "output.txt"}]
            }

        envelope = ToolEnvelope(func_with_artifacts)
        envelope.execute({})

        assert envelope.artifacts == [{"name": "output.txt"}]


class TestToolEnvelopeCallEnvelope:
    """Tests for ToolEnvelope.call_envelope() method."""

    @pytest.mark.production
    def test_call_envelope_structure(self, sample_tool_function):
        """Test that call_envelope returns correct structure."""
        envelope = ToolEnvelope(sample_tool_function)
        call_env = envelope.call_envelope()

        assert "name" in call_env
        assert "version" in call_env
        assert "description" in call_env
        assert "parameters" in call_env
        assert "required_parameters" in call_env
        assert "optional_parameters" in call_env
        assert "output_type" in call_env

    @pytest.mark.production
    def test_call_envelope_contains_correct_name(self, sample_tool_function):
        """Test call_envelope has correct name."""
        envelope = ToolEnvelope(sample_tool_function)
        call_env = envelope.call_envelope()

        assert call_env["name"] == "sample_add"

    @pytest.mark.production
    def test_call_envelope_contains_correct_version(self, sample_tool_function):
        """Test call_envelope has correct version."""
        envelope = ToolEnvelope(sample_tool_function)
        call_env = envelope.call_envelope()

        assert call_env["version"] == "1.0.0"

    @pytest.mark.production
    def test_call_envelope_parameters_have_metadata(self, sample_tool_function):
        """Test that parameters in call_envelope have metadata."""
        envelope = ToolEnvelope(sample_tool_function)
        call_env = envelope.call_envelope()

        assert "a" in call_env["parameters"]
        assert "kind" in call_env["parameters"]["a"]
        assert "default" in call_env["parameters"]["a"]
        assert "annotation" in call_env["parameters"]["a"]


class TestToolEnvelopeResultEnvelope:
    """Tests for ToolEnvelope.result_envelope() method."""

    @pytest.mark.production
    def test_result_envelope_structure(self, sample_tool_function):
        """Test that result_envelope returns correct structure."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.execute({"a": 1, "b": 2})
        result_env = envelope.result_envelope()

        assert "status" in result_env
        assert "message" in result_env
        assert "data" in result_env
        assert "citations" in result_env
        assert "artifacts" in result_env

    @pytest.mark.production
    def test_result_envelope_contains_execution_results(self, sample_tool_function):
        """Test result_envelope contains actual execution results."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.execute({"a": 10, "b": 5})
        result_env = envelope.result_envelope()

        assert result_env["status"] is True
        assert result_env["data"] == {"result": 15}
        assert result_env["message"] == "Addition successful"


class TestToolEnvelopeGetters:
    """Tests for getter methods."""

    @pytest.mark.production
    def test_get_name(self, sample_tool_function):
        """Test get_name method."""
        envelope = ToolEnvelope(sample_tool_function)
        assert envelope.get_name() == "sample_add"

    @pytest.mark.production
    def test_get_tool_version(self, sample_tool_function):
        """Test get_tool_version method."""
        envelope = ToolEnvelope(sample_tool_function)
        assert envelope.get_tool_version() == "1.0.0"

    @pytest.mark.production
    def test_get_description(self, sample_tool_function):
        """Test get_description method."""
        envelope = ToolEnvelope(sample_tool_function)
        assert "Add two numbers" in envelope.get_description()

    @pytest.mark.production
    def test_get_parameters(self, sample_tool_function):
        """Test get_parameters method."""
        envelope = ToolEnvelope(sample_tool_function)
        params = envelope.get_parameters()
        assert "a" in params
        assert "b" in params
        assert "optional" in params

    @pytest.mark.production
    def test_get_required_parameters(self, sample_tool_function):
        """Test get_required_parameters method."""
        envelope = ToolEnvelope(sample_tool_function)
        required = envelope.get_required_parameters()
        assert "a" in required
        assert "b" in required

    @pytest.mark.production
    def test_get_optional_parameters(self, sample_tool_function):
        """Test get_optional_parameters method."""
        envelope = ToolEnvelope(sample_tool_function)
        optional = envelope.get_optional_parameters()
        assert "optional" in optional

    @pytest.mark.production
    def test_get_result_status(self, sample_tool_function):
        """Test get_result_status method."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.execute({"a": 1, "b": 1})
        assert envelope.get_result_status() is True

    @pytest.mark.production
    def test_get_result_message(self, sample_tool_function):
        """Test get_result_message method."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.execute({"a": 1, "b": 1})
        assert envelope.get_result_message() == "Addition successful"

    @pytest.mark.production
    def test_get_result_data(self, sample_tool_function):
        """Test get_result_data method."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.execute({"a": 3, "b": 4})
        assert envelope.get_result_data() == {"result": 7}


class TestToolEnvelopeSetters:
    """Tests for setter methods."""

    @pytest.mark.production
    def test_set_result_status(self, sample_tool_function):
        """Test set_result_status method."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.set_result_status(False)
        assert envelope.result_status is False

    @pytest.mark.production
    def test_set_result_message(self, sample_tool_function):
        """Test set_result_message method."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.set_result_message("Custom message")
        assert envelope.result_message == "Custom message"

    @pytest.mark.production
    def test_set_result_data(self, sample_tool_function):
        """Test set_result_data method."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.set_result_data([{"key": "value"}])
        assert envelope.result_data == [{"key": "value"}]

    @pytest.mark.production
    def test_set_result_citations(self, sample_tool_function):
        """Test set_result_citations method."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.set_result_citations([{"source": "citation"}])
        assert envelope.citations == [{"source": "citation"}]

    @pytest.mark.production
    def test_set_result_artifacts(self, sample_tool_function):
        """Test set_result_artifacts method."""
        envelope = ToolEnvelope(sample_tool_function)
        envelope.set_result_artifacts([{"file": "artifact.txt"}])
        assert envelope.artifacts == [{"file": "artifact.txt"}]
