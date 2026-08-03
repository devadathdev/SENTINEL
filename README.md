# SENTINEL - Personal Digital Security AI

A comprehensive personal digital security platform with phishing analysis, breach monitoring, threat intelligence enrichment, and automated response capabilities.

## Architecture

```
SENTINEL/
├── sentinel/
│   ├── apps/
│   │   ├── api/          # FastAPI backend service
│   │   └── web/          # Next.js frontend dashboard
│   └── packages/
│       ├── schemas/      # Shared Pydantic schemas
│       └── security-sdk/ # Security utilities (encryption, JWT, audit chains)
├── docker-compose.yml    # Local development stack
├── Makefile             # Common development tasks
└── .env.example         # Environment configuration template
```

## Features

### Core Capabilities
- **Phishing Analysis** - Multi-vector analysis (URL structure, content, email headers)
- **Breach Monitoring** - Check email/identifier exposure against breach databases
- **Threat Intelligence Enrichment** - Enrich indicators (URLs, domains, IPs, hashes) via multiple connectors
- **Risk Scoring** - Multi-dimensional risk engine (identity, device, network, exposure, threat, context)
- **Policy Engine** - Action approval workflows with risk-based approval requirements
- **Action Execution** - Automated response actions (quarantine, disable, revoke, rotate, etc.)
- **Audit Logging** - Tamper-evident audit chain with HMAC-based integrity

### API Endpoints

#### Authentication
```
POST   /api/v1/auth/login          # User login
POST   /api/v1/auth/register       # User registration
POST   /api/v1/auth/refresh        # Refresh access token
POST   /api/v1/auth/logout         # Logout
GET    /api/v1/auth/me             # Current user info
```

#### Assets
```
GET    /api/v1/assets              # List assets
POST   /api/v1/assets              # Create asset
POST   /api/v1/assets/bulk         # Bulk create assets
PATCH  /api/v1/assets/{id}         # Update asset
DELETE /api/v1/assets/{id}         # Delete asset
```

#### Findings
```
GET    /api/v1/findings            # List findings (filterable by severity, status)
POST   /api/v1/findings            # Create finding
GET    /api/v1/findings/{id}       # Get finding details
PATCH  /api/v1/findings/bulk       # Bulk update findings
```

#### Phishing Analysis
```
POST   /api/v1/analyze/phishing    # Analyze text/email/URLs for phishing
```

#### Threat Intelligence
```
POST   /api/v1/indicators/enrich   # Enrich indicators (URL, domain, IP, hash)
```

#### Breach Monitoring
```
POST   /api/v1/breach/monitor      # Check identifier exposure
```

#### Incidents
```
GET    /api/v1/incidents           # List incidents
GET    /api/v1/incidents/{id}      # Get incident details
```

#### Actions
```
GET    /api/v1/actions             # List action proposals
POST   /api/v1/actions             # Create action proposal
GET    /api/v1/actions/{id}        # Get action details
POST   /api/v1/actions/{id}/approve # Approve & execute action
POST   /api/v1/actions/{id}/reject  # Reject action
```

#### Audit
```
GET    /api/v1/audit               # List audit events
```

#### Dashboard
```
GET    /api/v1/dashboard           # Security posture dashboard
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Node.js 20+ (for web development)

### Using Docker Compose (Recommended)

```bash
# Start all services
make dev

# Or manually:
docker-compose up -d

# Services available at:
# API:      http://localhost:8000
# Web:      http://localhost:3000
# PostgreSQL: localhost:5432
# Redis:    localhost:6379
```

### Local Development

```bash
# Install dependencies
make install

# Start API locally
make dev-api

# Start Web locally (in another terminal)
make dev-web

# Run database migrations
make db-migrate
```

### Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT signing key (generate with `openssl rand -hex 32`)
- `THREAT_INTEL_API_KEYS` - JSON dict of API keys (virustotal, abuseipdb, etc.)
- `BREACH_API_KEYS` - JSON dict of breach API keys (haveibeenpwned)
- `AI_API_KEY` - OpenAI/Anthropic API key for AI explanations

## Development

### Running Tests

```bash
# All tests
make test

# API tests only
make test-api

# Web tests only
make test-web
```

### Linting & Type Checking

```bash
# Lint (ruff, eslint)
make lint

# Type check (mypy, tsc)
make typecheck

# Format code
make fmt
```

### Database Operations

```bash
# Run migrations
make db-migrate

# Create new migration
make db-revision MSG="description"

# Reset database (destructive!)
make db-reset
```

### Building

```bash
# Build Docker images
make build

# Build API image
make build-api

# Build Web image
make build-web
```

## Project Structure Details

### API Service (`sentinel/apps/api/`)

```
sentinel_api/
├── main.py              # FastAPI app factory
├── config.py            # Pydantic settings
├── auth.py              # JWT authentication
├── database.py          # SQLAlchemy models & session
├── routes.py            # API route handlers
├── routes/
│   └── auth.py          # Auth endpoints
├── services/
│   ├── policy.py        # Policy engine
│   ├── executor.py      # Action executors
│   ├── risk.py          # Risk scoring engine
│   ├── graph.py         # Security graph service
│   └── audit.py         # Audit logging
├── workers/
│   ├── phishing.py      # Phishing analysis worker
│   └── enrichment.py    # Threat intel enrichment
├── connectors/
│   └── breach.py        # Breach monitoring connectors
└── tests/               # Pytest test suite
```

### Web Dashboard (`sentinel/apps/web/`)

Next.js 14 App Router with:
- Dashboard - Security posture overview
- Assets - Asset inventory & criticality
- Findings - Finding management & triage
- Incidents - Incident timeline & investigation
- Phishing - Interactive phishing analyzer
- Settings - User preferences & API keys

### Shared Packages

**schemas** (`sentinel/packages/schemas/`)
- All Pydantic models for API contracts
- Event envelopes with hash chaining
- Enums for severity, action classes, statuses

**security-sdk** (`sentinel/packages/security-sdk/`)
- Symmetric/asymmetric encryption
- JWT token management
- Audit chain with HMAC integrity
- Secure password hashing
- Constant-time comparison

## Security Considerations

- All passwords hashed with HKDF-SHA256 + salt
- JWT tokens with short expiry (30min access, 7day refresh)
- Refresh tokens stored in HttpOnly cookies
- CORS restricted to configured origins
- Audit events cryptographically chained
- Input validation on all endpoints
- Rate limiting ready (configure via settings)

## API Documentation

When running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT# SENTINEL
