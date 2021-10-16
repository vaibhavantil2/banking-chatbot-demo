FROM lambci/lambda:build-nodejs12.x

ENV AWS_DEFAULT_REGION us-east-1
ENV DOCKER_LAMBDA_STAY_OPEN 1

COPY . .

RUN npm install

RUN zip -9yr lambda.zip .

CMD aws lambda update-function-code --function-name webhook --zip-file fileb://lambda.zip
