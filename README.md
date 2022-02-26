## Cookiecutter template for Python CDK Stack project

This is a cookiecutter template for AWS infrastructure stack project using AWS CDK for Python.

The [poetry](https://python-poetry.org/) package manager should exist in PATH in order to use this template.

The main dependecnies for the generated project are:
1. [AWS Cloud Development Kit](https://aws.amazon.com/cdk/) for Python
2. [AWS Lambda Powertools for Python](https://awslabs.github.io/aws-lambda-powertools-python/latest/)
3. pytest

The following linting tools are also required and preconfigured to use with the generated project:
* flake8
* isort
* black
* mypy
* pre-commit


Visual Studio Code is the preferred editor for the author and the [settings]({{cookiecutter.pkg_name}}/.vscode/settings.json) are provided for quick startup. 

To use the template, please install cookiecutter on your computer by following [instructions here](https://cookiecutter.readthedocs.io/en/latest/installation.html)

```

# generate the template, enter project name when prompted
cookiecutter gh:vino9org/cookiecutter-python-cdk-stack

# init venv and install dependencies
cd <project_path>
poetry shell
poetry install

# kick the tires...
pytest -v

# hack away!

```

[A Github action pipeline]({{cookiecutter.pkg_name}}/.github/workflows/pipeline.yaml) is also generated. The following secrets are required for the pipeline to work:
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY

### TODO:
1. add GitLab pipeline
2. make cdk and other dependecnies version configurable
