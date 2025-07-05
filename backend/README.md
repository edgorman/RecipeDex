# backend

## Running

Get a bearer token from frontend

To make requests to local endpoints run

```bash
make backend-run-service
```

To make requests to deployed endpoints run:

```bash
make backend-proxy-service GCP_PROJECT_ID=<your-project-id> GCP_PROJECT_REGION=<your-project-region>
```

And then run your request:

```bash
make backend-call-service TOKEN=<your-token-here> ENDPOINT=protected
```
