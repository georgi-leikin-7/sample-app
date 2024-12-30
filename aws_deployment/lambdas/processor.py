class ProcessorLambda:

    def __init__(self):
        self.name: str = "processor-app"
        self.context_path: str = "../"
        self.docker_file: str = "lambdas/processor/Dockerfile"
        self.setup_api_gateway: bool = False
