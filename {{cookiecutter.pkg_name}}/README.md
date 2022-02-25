
# Welcome to your CDK Python project!

This project is set up like Python project using poetry package manager. 

The `cdk.json` file tells the CDK Toolkit how to execute your app.


## Setup
```
# create virtualenv
$ poetry shell

# install dependencies
(.venv)$ poetry install

```

## Develop the code for the stack
```
# run unit tests
pytest

# use cdk to deploy infrastructure
# ensure your AWS credentials are set, then
cdk synth
cdk deploy

```

## push to Github
```
poetry export -o requirements.txt
# push to feature branches and develop branch will trigger pipeline run
git push ...