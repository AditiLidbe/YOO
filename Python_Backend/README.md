## Talenta Python Backend

This backend handles the Python side of Talenta:

- Module 2: jobs and applications
- Module 3: AI screening

Java handles authentication. The frontend should call the API Gateway, not this
service directly.

## Service Ports

```text
Frontend       -> API Gateway      : http://localhost:8080
API Gateway    -> Java Auth        : http://localhost:8081
API Gateway    -> Python Backend   : http://localhost:8000
Python Backend -> PostgreSQL
Java Backend   -> PostgreSQL
```

## Environment

Create `.env` inside `Python_Backend`.

```env
DATABASE_URL=postgresql://postgres:PASSWORD@HOST:PORT/talenta
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET_NAME=
AWS_REGION=ap-south-1
```

For your ngrok PostgreSQL URL, the format should be:

```text
postgresql://postgres:PASSWORD@0.tcp.in.ngrok.io:17114/talenta
```

## Run Python Backend

```bash
cd Python_Backend
uv sync
uv run alembic upgrade head
uv run uvicorn main:app --reload --port 8000
```

If you are not using `uv`, install the dependencies in your virtual environment
and run:

```bash
alembic upgrade head
uvicorn main:app --reload --port 8000
```

## Gateway Flow

Java auth creates the JWT. The gateway validates the JWT and sends these headers
to Python:

```text
X-User-Id
X-Role
```

Python uses those headers to check whether the current user is a recruiter,
candidate, or admin.

## Main Python Routes Through Gateway

```text
POST   /api/jobs
GET    /api/jobs
GET    /api/jobs/open
GET    /api/jobs/{job_id}
PATCH  /api/jobs/{job_id}
DELETE /api/jobs/{job_id}

POST   /api/jobs/{job_id}/apply
GET    /api/candidates/me/applications
GET    /api/recruiters/me/applications
GET    /api/applications/{application_id}
GET    /api/applications/{application_id}/resume-url
PATCH  /api/applications/{application_id}/status

GET    /api/ai/applications/{application_id}
```

Apply to job uses `multipart/form-data`:

```text
cover_letter: text
resume: file
```

The uploaded resume is stored privately in S3. The API saves only the S3 object
path in the database. To view/download it, call the resume URL endpoint and use
the temporary presigned URL.
