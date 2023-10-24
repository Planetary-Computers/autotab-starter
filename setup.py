from setuptools import setup, find_packages

setup(
    name="autotab",
    version="0.1",
<<<<<<< HEAD
    packages=find_packages(),
=======
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
>>>>>>> 2e1156ddd94cef91243cab43e4bfb8eacea7bacc
    entry_points={
        "console_scripts": [
            "autotab = main:main",
        ],
    },
)
