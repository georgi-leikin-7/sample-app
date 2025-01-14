class FastApiLambda:

    def __init__(self):
        self.name: str = "fast-api-app"
        self.context_path: str = "../"
        self.docker_file: str = "lambdas/fast_api/Dockerfile"
        self.setup_api_gateway: bool = True
        self.domain_name: str = "api.facade"
