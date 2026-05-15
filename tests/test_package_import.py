import pytest
import unlearning_benchmark

def test_package_import():
    """Test that the package can be imported and has a version string."""
    assert unlearning_benchmark is not None
    assert hasattr(unlearning_benchmark, "__version__")
    assert isinstance(unlearning_benchmark.__version__, str)
