"""
    Setup file for BARCAnalytics.
"""
from setuptools import setup

if __name__ == "__main__":
    try:
        setup()
    except:  # noqa
        print(   # noqa: T201, T001
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools wheel\n\n"
        )
        raise
