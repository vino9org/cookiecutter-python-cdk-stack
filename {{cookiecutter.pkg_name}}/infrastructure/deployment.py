import os

import aws_cdk as cdk

from {{ cookiecutter.pkg_name }} import {{ cookiecutter.stack_name }}

stack_name = os.environ.get("TESTING_STACK_NAME", "{{ cookiecutter.stack_name }}")
app = cdk.App()
{{ cookiecutter.stack_name }}(app, stack_name).build()
app.synth()
