from pip.req import parse_requirements
from setuptools import setup, find_packages

def get_test_suite():
    """
    Prepare a test-suite callable with:
        python setup.py test
    """
    import unittest
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


def load_requirements():
    """ Helps to avoid storing requirements in more than one file"""
    reqs = parse_requirements('requirements-to-freeze.txt', session=False)
    reqs_list = [str(ir.req) for ir in reqs]
    return reqs_list

setup(
    name="proj",

    use_scm_version=True,
    url="https://github.com/...",
    license="MIT",
    author="...",
    author_email="...",
    description="...",
    long_description=__doc__,
    keywords=["..."],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    platforms="any",  # darwin, linux2
    setup_requires=["setuptools_scm"],
    install_requires=load_requirements(),
    # tests_require=["mock", "pytest-cov"],  # requirements included above
    test_suite="setup.get_test_suite",

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ],

    entry_points={
        "console_scripts": [
            "runit = proj.main:main",
        ],
    },
)
