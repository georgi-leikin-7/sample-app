from uuid import uuid4

from aws_cdk import IgnoreMode, Stack, aws_apigateway, aws_lambda, aws_certificatemanager
from aws_cdk.aws_lambda import IFunction
from constructs import Construct

from lambdas.fast_api import FastApiLambda
from lambdas.fast_api_processor import FastApiProcessorLambda


class AwsDeploymentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        for lambda_ in [FastApiLambda(), FastApiProcessorLambda()]:

            lambda_function = aws_lambda.DockerImageFunction(
                scope=self,
                id=f"{lambda_.name}-{uuid4()}",
                function_name=lambda_.name,
                code=aws_lambda.DockerImageCode.from_image_asset(
                    directory=lambda_.context_path,
                    file=lambda_.docker_file,
                    ignore_mode=IgnoreMode.GLOB,
                ),
            )

            if lambda_.setup_api_gateway:
                i_function: IFunction = aws_lambda.Function.from_function_arn(
                    scope=self,
                    id=f"{lambda_.name}-function-arn",
                    function_arn=lambda_function.function_arn,
                )

                rest_api = aws_apigateway.RestApi(
                    scope=self,
                    id=f"{lambda_.name}-rest-api",
                    rest_api_name=f"{lambda_.name}-rest-api",
                    deploy_options=aws_apigateway.StageOptions(stage_name="local"),
                    endpoint_types=[aws_apigateway.EndpointType.REGIONAL],
                )

                resource = rest_api.root.add_proxy(
                    any_method=True,
                    default_integration=aws_apigateway.LambdaIntegration(handler=i_function),
                )

                allowed_headers = "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,x-correlation-id"
                allowed_origins = "*"
                allowed_methods = "OPTIONS,GET,POST,PUT,DELETE"

                options_integration = aws_apigateway.MockIntegration(
                    integration_responses=[
                        aws_apigateway.IntegrationResponse(
                            status_code="200",
                            response_parameters={
                                "method.response.header.Access-Control-Allow-Headers": f"'{allowed_headers}'",
                                "method.response.header.Access-Control-Allow-Origin": f"'{allowed_origins}'",
                                "method.response.header.Access-Control-Allow-Methods": f"'{allowed_methods}'",
                            },
                        )
                    ],
                    request_templates={"application/json": '{"statusCode": 200}'},
                )

                resource.add_method(
                    "OPTIONS",
                    options_integration,
                    method_responses=[
                        aws_apigateway.MethodResponse(
                            status_code="200",
                            response_parameters={
                                "method.response.header.Access-Control-Allow-Headers": True,
                                "method.response.header.Access-Control-Allow-Origin": True,
                                "method.response.header.Access-Control-Allow-Methods": True,
                            },
                        )
                    ],
                )

                certificate = aws_certificatemanager.Certificate(
                    scope=self,
                    id=f"{lambda_.name}-certificate",
                    domain_name="api.example.com",
                    validation=aws_certificatemanager.CertificateValidation.from_dns()
                )

                domain_name = aws_apigateway.DomainName(
                    scope=self,
                    id=f"{lambda_.name}-domain-name",
                    domain_name="api.example.com",
                    certificate=certificate,
                    endpoint_type=aws_apigateway.EndpointType.REGIONAL
                )

                aws_apigateway.BasePathMapping(
                    scope=self,
                    id=f"{lambda_.name}-path-mapping",
                    domain_name=domain_name,
                    rest_api=rest_api,
                    stage=rest_api.deployment_stage
                )
