import json
import os
import shlex
import shutil
import subprocess

context = json.loads(
    """
{{ cookiecutter | jsonify }}
"""
)

is_lambda_used = context["use_lambda"] == "y"

if not is_lambda_used:
    shutil.rmtree("runtime")
    shutil.rmtree("tests/unit/runtime")

# .env file will be used by VS Code with the setting provided in the project
# setting PYTHONPATH will let VS Code load modules from the right path
with open(".env", "w") as env_f:
    env_f.write("PYTHONPATH=infrastructure")
    if is_lambda_used:
        env_f.write(":runtime")
    env_f.write("\n")

# fix the stack name in pipeline. it is in Jinja2 format, too much quoting needed
# to make it a template itself
# OSX and Linux sed has different syntax for inline editing so we use a intermediary file
# instead
with open(".github/workflows/pipeline.yaml", "w") as out_f:
    subprocess.call(
        shlex.split(
            "sed 's/DUMMYSTACKNAME/{{ cookiecutter.stack_name }}/g' .github/workflows/pipeline.yaml.pre"
        ),
        stdout=out_f,
    )
os.unlink(".github/workflows/pipeline.yaml.pre")


# create a git repo, everybody needs this, right?
subprocess.call(["git", "init"])
subprocess.call(["git", "add", ".gitignore"])
subprocess.call(["git", "add", "*"])
subprocess.call(["git", "commit", "-m", "generated by cookiecutter"])

# print some help messages
home = os.path.expanduser("~")
relpath = os.path.relpath(os.getcwd(), home)
print(
    f"""
# To start working on the project,

cd ~/{relpath}
poetry install
poetry run precommit install
poetry shell


#    Hack away!

"""
)
