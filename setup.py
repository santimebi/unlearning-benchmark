from setuptools import setup, find_packages

setup(
    name="unlearning_benchmark",
    version="0.1.0",
    description="A framework for machine unlearning evaluation and benchmarking.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.2.0",
        "pyyaml>=6.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black",
            "ruff"
        ]
    },
    python_requires=">=3.10",
)
