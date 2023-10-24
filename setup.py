from setuptools import setup

setup(
    name="autotab",
    description="Build browser agents for real world tasks.",
    version="0.1.0",
    py_modules=["autotab"],
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "autotab = main:main",
        ],
    },
)
