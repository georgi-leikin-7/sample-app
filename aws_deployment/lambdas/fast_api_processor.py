class FastApiProcessorLambda:

    def __init__(self):
        self.name: str = "fast-api-processor"
        self.context_path: str = "../"
        self.docker_file: str = "lambdas/fast_api_processor/Dockerfile"
        self.setup_api_gateway: bool = False
