#!/usr/bin/env bash

# Execute CDK project
pip install -r /var/lib/localstack/aws_deployment/requirements.txt
cd /var/lib/localstack/aws_deployment && cdklocal bootstrap --app "python3 app.py"
cd /var/lib/localstack/aws_deployment && cdklocal deploy --app "python3 app.py" --require-approval never