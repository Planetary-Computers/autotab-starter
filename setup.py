from setuptools import setup, find_packages

setup(
    name="autotab",
    description="Build browser agents for real world tasks.",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "autotab = main:main",
        ],
    },
)
