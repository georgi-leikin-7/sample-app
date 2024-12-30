FROM amazon/aws-lambda-python:3.11

COPY lambdas/fast_api_processor/app.py ${LAMBDA_TASK_ROOT}
COPY lambdas/fast_api_processor/requirements.txt ${LAMBDA_TASK_ROOT}

COPY facade_lib /facade_lib

RUN pip install -r requirements.txt
RUN pip install /facade_lib

CMD [ "app.handler" ]