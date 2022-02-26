import aws_cdk as core
import aws_cdk.assertions as assertions
from {{ cookiecutter.pkg_name }} import {{ cookiecutter.stack_name }}


def test_stack_created():
    app = core.App()
    stack = {{ cookiecutter.stack_name }}(app, "{{ cookiecutter.stack_name }}")
    template = assertions.Template.from_stack(stack)
    assert template
