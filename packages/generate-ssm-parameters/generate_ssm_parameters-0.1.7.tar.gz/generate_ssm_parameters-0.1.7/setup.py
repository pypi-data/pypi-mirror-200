from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="generate_ssm_parameters",
    version="0.1.7",
    description="A script for creating AWS SSM Parameters in bulk from a CSV file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/travers-co/generate-ssm-parameters",
    author="Travers Annan",
    author_email="travers@curiousorbit.com",
    license="MIT",
    packages=[
        "generate_ssm_parameters"
    ],
    py_modules=[
        "gen_ssm_params"
    ],
    install_requires=[
        "boto3 > 1.24.0",
        "botocore > 1.12.0",
        "click > 7.0.0",
        "pandas > 1.1.5",
        "tqdm > 4.0.0",
    ],
    python_requires='>=3.7',
    # - dashes in the second half of this cause module not found errors, not supported
    entry_points={
        "console_scripts": [
            "generate-ssm-parameters=generate_ssm_parameters.gen_ssm_params:cli"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)
