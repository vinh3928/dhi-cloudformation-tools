# Examples

Example Lambda infrastructure.

Requires the full cycle to be deployed, Validate > Package > Deploy.

## Run

1. Build
```sh
python3 -m zipfile -c code.zip code/*
```

2. Deploy
```sh
cfn deploy --template infrastructure/main.yml --config infrastructure/config.json --s3-bucket <s3-bucket>
```
