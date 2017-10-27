"""
Goal: provide access to the version information
"""

DEFAULT_VERSION = 'unknown'

try:
    import pkg_resources
    try:
        __VERSION__ = pkg_resources.require("proj")[0].version
    except Exception:
        __VERSION__ = DEFAULT_VERSION
except Exception:
    from setuptools_scm import get_version
    try:
        __VERSION__ = get_version()
    except Exception:
        __VERSION__ = DEFAULT_VERSION


if __name__ == "__main__":
    print(__VERSION__)
