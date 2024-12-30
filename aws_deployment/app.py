import aws_cdk as cdk

from aws_deployment.aws_deployment_stack import AwsDeploymentStack

app = cdk.App()

AwsDeploymentStack(
    app,
    construct_id="AwsDeploymentStack",
    env=cdk.Environment(account="000000000000", region="us-east-1"),
)

app.synth()
