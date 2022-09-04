import os
import os.path
import shlex
import subprocess


def assert_pipeline_yaml(project_path):
    # check if pipeline.yaml handled correctly by post_gen_project hook
    with open(f"{project_path}/.github/workflows/pipeline.yaml", "r") as f:
        content = "".join(f.readlines())
        assert "DUMMYSTACKNAME" not in content
    assert not os.path.isfile(f"{project_path}/.github/workflows/pipeline.yaml.pre")


def run_command(project_path, command):
    if not os.path.isdir(project_path):
        return

    try:
        current_path = os.getcwd()

        os.chdir(project_path)
        subprocess.call(["poetry", "install"])

        # execute the command. if the command fails, print stdout and stderr
        # for debugging purposes
        result = subprocess.run(shlex.split(command), capture_output=True)
        if result.returncode != 0:
            print(f"error when running '{command}'")
            print(result.stdout.decode("utf-8"))

        assert result.returncode == 0
    finally:
        os.chdir(current_path)


def run_pytest_in_generated_project(project_path):
    run_command(project_path, "poetry run pytest -v tests/unit")


def run_flake8_in_generated_project(project_path):
    run_command(project_path, "poetry run flake8")


def run_mypy_in_generated_project(project_path):
    run_command(project_path, "poetry run mypy infrastructure")


def test_default_project(cookies):
    result = cookies.bake(extra_context={"project_name": "My Default Stack"})

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "my-default-stack"
    assert result.project_path.is_dir()

    print(f"test project generated {result.project_path}")

    assert_pipeline_yaml(result.project_path)

    # project default does not generate lambda funciton
    assert not os.path.exists(f"{result.project_path}/runtime")
    assert not os.path.exists(f"{result.project_path}/tests/runtime")

    run_pytest_in_generated_project(result.project_path)
    # run_flake8_in_generated_project(result.project_path)
    run_mypy_in_generated_project(result.project_path)


def test_lambda_project(cookies):
    result = cookies.bake(
        extra_context={"project_name": "My Lambda Stack", "use_lambda": "y"}
    )

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "my-lambda-stack"
    assert result.project_path.is_dir()

    print(f"test project generated {result.project_path}")

    # should be replaced by post_gen_project hook
    assert_pipeline_yaml(result.project_path)

    # these diretories should exist when lambda function is enabeld
    assert os.path.isfile(f"{result.project_path}/runtime/app.py")
    assert os.path.isdir(f"{result.project_path}/tests/unit/runtime")

    run_pytest_in_generated_project(result.project_path)
    # run_flake8_in_generated_project(result.project_path)
    run_mypy_in_generated_project(result.project_path)
