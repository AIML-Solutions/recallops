# Operations

RecallOps is intended to run as a service that can be attached to internal tools.

The default verified path uses the in-memory reference index. Docker Compose also starts Postgres and Qdrant so durable metadata and ANN index adapters can be exercised as they are added.

## Local Service

```bash
docker compose up --build
```

## Health

```bash
curl http://localhost:8000/health
```

## Testing

```bash
make test
make smoke
```

## Deployment Notes

Organization-specific deployments should add authentication, authorization, retention policy, audit logging, and access enforcement before indexing restricted content into shared collections.
