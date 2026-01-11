"""
Tests for decorators in src/ai_tools/utilities/decorators.py

Production-ready component - all tests should pass.
"""

import pytest
from ai_tools.utilities.decorators import version


class TestVersionDecorator:
    """Tests for the @version decorator."""

    @pytest.mark.production
    def test_version_adds_attribute_to_function(self):
        """Test that @version adds __version__ to decorated function."""
        @version("1.2.3")
        def sample_func():
            return "hello"

        assert hasattr(sample_func, "__version__")
        assert sample_func.__version__ == "1.2.3"

    @pytest.mark.production
    def test_version_preserves_function_behavior(self):
        """Test that decorated function still works correctly."""
        @version("1.0.0")
        def add(a, b):
            return a + b

        result = add(2, 3)
        assert result == 5

    @pytest.mark.production
    def test_version_preserves_function_name(self):
        """Test that @version preserves function __name__."""
        @version("1.0.0")
        def my_function():
            pass

        assert my_function.__name__ == "my_function"

    @pytest.mark.production
    def test_version_preserves_docstring(self):
        """Test that @version preserves function docstring."""
        @version("1.0.0")
        def documented_func():
            """This is the docstring."""
            pass

        assert documented_func.__doc__ == "This is the docstring."

    @pytest.mark.production
    def test_version_works_on_classes(self):
        """Test that @version works on class definitions."""
        @version("2.0.0")
        class MyClass:
            pass

        assert hasattr(MyClass, "__version__")
        assert MyClass.__version__ == "2.0.0"

    @pytest.mark.production
    def test_version_rejects_invalid_format_missing_patch(self):
        """Test that invalid version format (missing patch) raises ValueError."""
        with pytest.raises(ValueError, match="Invalid version"):
            @version("1.0")
            def bad_version():
                pass

    @pytest.mark.production
    def test_version_rejects_non_semver_with_prefix(self):
        """Test that non-semver strings with 'v' prefix are rejected."""
        with pytest.raises(ValueError, match="Invalid version"):
            @version("v1.0.0")
            def bad_version():
                pass

    @pytest.mark.production
    def test_version_rejects_text_version(self):
        """Test that text versions are rejected."""
        with pytest.raises(ValueError, match="Invalid version"):
            @version("one.two.three")
            def bad_version():
                pass

    @pytest.mark.production
    def test_version_accepts_valid_semver_zero(self):
        """Test valid semver with zeros."""
        @version("0.0.1")
        def func1():
            pass

        assert func1.__version__ == "0.0.1"

    @pytest.mark.production
    def test_version_accepts_valid_semver_large_numbers(self):
        """Test valid semver with large numbers."""
        @version("10.20.30")
        def func2():
            pass

        assert func2.__version__ == "10.20.30"

    @pytest.mark.production
    def test_decorated_function_accepts_args_and_kwargs(self):
        """Test that decorated function handles *args and **kwargs."""
        @version("1.0.0")
        def flexible_func(*args, **kwargs):
            return args, kwargs

        result = flexible_func(1, 2, 3, key="value")
        assert result == ((1, 2, 3), {"key": "value"})
