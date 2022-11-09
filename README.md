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

Check out the [Serverless Framework docs](https://www.serverless.com/framework/docs/providers/aws/cli-reference/invoke/) for more information.

### Local development

You can invoke your function locally by using the following command:

```bash
serverless invoke local --function hello
```

Which should result in response similar to the following:

```
{
    "statusCode": 200,
    "body": "{\"message\": \"Go Serverless v3.0! Your function executed successfully!\", \"input\": {}}"
}
```

### Bundling dependencies

In case you would like to include third-party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).
