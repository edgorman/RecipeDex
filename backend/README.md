# backend

## Service

### Running

Get a bearer token from frontend

To make requests to local endpoints run:

```bash
make backend run-service
```

To make requests to deployed endpoints run:

```bash
make backend proxy-service GCP_PROJECT_ID=<your-project-id> GCP_PROJECT_REGION=<your-project-region>
```

And then run your request:

```bash
make backend call-service TOKEN=<your-token-here> ENDPOINT=protected
```

## Linting

To lint the backend run

```bash
make backend lint
```

## Testing

To test the backend run

```bash
make backend test
```

## Agents

### Running

To run the agent sdk web view, run:

```bash
make backend-run-agent
```
