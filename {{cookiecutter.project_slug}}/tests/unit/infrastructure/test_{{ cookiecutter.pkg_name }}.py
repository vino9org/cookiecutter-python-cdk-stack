import os

import aws_cdk as cdk
import aws_cdk.assertions as assertions
import pytest
from aws_cdk.assertions import Template

from {{ cookiecutter.pkg_name }} import {{ cookiecutter.stack_name }}


@pytest.fixture(scope="session")
def stack() -> Template:
    stack_name = os.environ.get("TESTING_STACK_NAME", "{{ cookiecutter.stack_name }}")
    app = cdk.App()
    stack = {{ cookiecutter.stack_name }}(app, "{{ cookiecutter.stack_name }}")
    return assertions.Template.from_stack(stack)

def test_stack_created(stack):
    assert stack
