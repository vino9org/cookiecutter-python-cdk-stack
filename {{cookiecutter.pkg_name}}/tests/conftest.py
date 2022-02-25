import os
import sys

cwd = os.path.dirname(os.path.abspath(__file__))
{% if cookiecutter.use_lambda == 'y' -%}
sys.path.insert(0, os.path.abspath(f"{cwd}/../runtime"))
{%- endif %}
sys.path.insert(0, os.path.abspath(f"{cwd}/../infrastructure"))
