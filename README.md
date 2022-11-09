# AWS Serverless Thumbnail Service

<img width="1291" alt="docs" src="https://user-images.githubusercontent.com/4117768/200938384-eab53fe6-6fab-4e5d-b192-50517b2502ff.png">

# Requirements

-   [Node.js](https://nodejs.org/en/
-   [Serverless Framework](https://www.serverless.com/framework/docs/getting-started/)
-   [AWS Account](https://aws.amazon.com/)
-   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
-   [Python3.8](https://www.python.org/downloads/release/python-380/)

## Usage

### Deployment

```
$ sls deploy
```

### Invocation

After successful deployment, you can invoke the deployed function by using the following command:

```bash
sls invoke --function health
```

Which should result in response similar to the following:

```json
{
    "statusCode": 200,
    "body": "{\"message\": \"ok\"}"
}
```

### Local development

You can invoke your function locally by using the following command:

```bash
sls invoke local --function health
```

Which should result in response similar to the following:

```
{
    "statusCode": 200,
    "body": "{\"message\": \"ok\"}"
}
```

Check out the [Serverless Framework docs](https://www.serverless.com/framework/docs/providers/aws/cli-reference/invoke/) for more information.
