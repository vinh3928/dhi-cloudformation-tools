# dhi-cloudformation-tools

CLI tools for CloudFormation

## Installation
```sh
pip3 install --upgrade git+https://github.com/DiceHoldingsInc/dhi-cloudformation-tools.git
pip3 install --upgrade git+https://github.com/DiceHoldingsInc/dhi-cloudformation-tools.git@1.0.0
```

## Usage
```sh
cfn --help
cfn --version
```

#### Validate

Validates the specified AWS CloudFormation template.

```sh
cfn validate --help
cfn validate --template <main.yml>
cfn val -t <main.yml>
```

* `--template` - The path where your AWS CloudFormation template is located.
* `--config` - The path where your AWS CloudFormation template configuration is located.

#### Package

Validates and Packages the specified AWS CloudFormation template by creating and then executing a change set.

```sh
cfn package --help
cfn package --template <main.yml> --config <config.json> --s3-bucket <some-bucket>
cfn pkg -t <main.yml> -c <config.json> -b <some-bucket>
```

* `--template` - The path where your AWS CloudFormation template is located.
* `--config` -The path where your AWS CloudFormation template configuration is located.
* `--s3-bucket` - The name of the S3 bucket where this command uploads the artifacts that are referenced in your template.
* `--s3-prefix` - A prefix name that the command adds to the artifact's name when it uploads them to the S3 bucket.
* `--kms-key-id` - The ID of an AWS KMS key that the command uses to encrypt artifacts that are at rest in the S3 bucket.
* `--output-template-file` - The path to the file where the command writes the output AWS CloudFormation template.
* `--approve` - Approve command execution and bypass manual confirmation.

#### Deploy

Validates, Packages and Deploys the specified AWS CloudFormation template by creating and then executing a change set.

```sh
cfn deploy --help
cfn deploy --template <main.yml> --config <config.json> --s3-bucket <some-bucket>
cfn dpl -t <main.yml> -c <config.json> -b <some-bucket>
```

* `--template` - The path where your AWS CloudFormation template is located.
* `--config` -The path where your AWS CloudFormation template configuration is located.
* `--s3-bucket` - The name of the S3 bucket where this command uploads the artifacts that are referenced in your template.
* `--s3-prefix` - A prefix name that the command adds to the artifact's name when it uploads them to the S3 bucket.
* `--kms-key-id` - The ID of an AWS KMS key that the command uses to encrypt artifacts that are at rest in the S3 bucket.
* `--output-template-file` - The path to the file where the command writes the output AWS CloudFormation template.
* `--approve` - Approve command execution and bypass manual confirmation.

#### Deploy only

Deploys the specified AWS CloudFormation packaged template by creating and then executing a change set.

```sh
cfn deploy-only --help
cfn deploy-only --packaged <main.yml> --config <config.json> --approve
cfn dplo -k <packaged.yml> -c <config.json> -a
```

* `--packaged` - The path where your AWS CloudFormation packaged template is located.
* `--config` -The path where your AWS CloudFormation template configuration is located.
* `--approve` - Approve command execution and bypass manual confirmation.

#### AWS Profile
```sh
export AWS_PROFILE=<someprofile>
cfn val -t <main.yml>
```
or
```sh
cfn val --profile <someprofile> --template <main.yml>
cfn val -p <someprofile> -t <main.yml>
```

## Template and Configuration

#### Template

A template is a YAML-formatted text file that describes your AWS infrastructure.

[AWS CloudFormation Template Anatomy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html)

```yml
AWSTemplateFormatVersion: 2010-09-09

Description: Dummy Python Lambda

Parameters:
  # Tags
  Environment:
    Type: String
  Brand:
    Type: String
  Application:
    Type: String
  Owner:
    Type: String
  # ...

Resources:

  Lambda:
    Type: AWS::Lambda::Function
    Properties:
      # ...

  LambdaLogs:
    Type: AWS::Logs::LogGroup
    Properties:
      # ...

  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
      # ...

Outputs:
  # ...
```

#### Configuration

A template configuration file is a JSON-formatted text file that can specify template parameter values and tags. Use these configuration files to specify parameter values or a stack policy for a stack. All of the parameter values that you specify must be declared in the associated template.

[AWS CloudFormation Artifacts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html)

```js
{
  "Parameters" : {
    "Environment" : "test",
    "Brand" : "dhi",
    "Application" : "dummy",
    "Owner" : "cpe",
    "LogRetentionInDays" : 1,
    "LogLevel" : "debug"
  },
  "Tags" : {
    "Name": "test-dhi-dummy",
    "BusinessUnit": "dhi",
    "Application": "dummy",
    "Environment": "test",
    "Owner": "cpe"
  }
}
```

#### Conventions

This tool follows the DHI AWS Naming Conventions and Tagging Policies.

As a result of that, these are the required Parameters:

- Parameters `required`
  - Environment `required`
  - Brand `required`
  - Application `required`
  - Owner `required`

The computed elements used to simplify this tool's interface also follow the same conventions:

- Tags
  - Name `{Environment}-{Brand}-{Application}`
  - BusinessUnit `{Brand}`
  - Application `{Application}`
  - Environment `{Environment}`
  - Owner `{Owner}`
- Stack Name `{Environment}-{Brand}-{Application}`
- S3 prefix (Packaging) `{Environment}-{Brand}-{Application}`

## Examples

- [Lambda](examples)

## Development

#### Run
setup environment
```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -e .
```
and then use as normal
```sh
cfn --help
```

#### Tests

###### Unit

```sh
python3 setup.py test
```

## Reference

- [AWS CloudFormation Artifacts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html)
- [Python argparse](https://docs.python.org/3/library/argparse.html)

## Future

- generate config.json skeleton base on main.yml
- generate makrdown docs with params/resources/outputs
- add clean command --config
- output, resources and events
- instructions to spin multiple stacks of the same template
- awssaml logging, maybe provide example alias to combine with cfn
- termination protection, see if this is helpful
- drift (picks up loose resources)

## Owner

Cloud Platform Engineering (CPE)

cloud.platform.engineering@dhigroupinc.com
