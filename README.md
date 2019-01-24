* sam package --template-file template.yaml --s3-bucket colibri-digital-sam-bucket --output-template-file packaged.yaml
* sam deploy --template-file packaged.yaml --stack-name pycharm-demo --capabilities CAPABILITY_IAM
