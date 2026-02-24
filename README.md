# LSP Consent System - Module 3

A **FastAPI-based consent management backend** for the Loan Service Platform (LSP), ensuring RBI-compliant consent collection and legal document management. This module handles explicit user agreement to all mandatory legal documents before onboarding proceeds.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Setup & Installation](#setup--installation)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Development](#development)

---

## Overview

Module 3 is responsible for:
- Collecting explicit user consent for legal documents
- Managing multiple document versions
- Enforcing scroll-to-bottom validation
- Maintaining consent history and audit logs
- Supporting consent revocation
- Generating PDF downloads of legal documents

This module integrates with **Module 2** for user identification and maintains full compliance audit trails for regulatory requirements.

---

## Features

 **Data Consent Management**
- Terms & Conditions
- Privacy Policy
- Data Processing Consent
- Credit Bureau Consent

 **Document Management**
- PDF download capability for all legal documents
- Text API for frontend document display
- Document versioning and activation controls

 **Consent Enforcement**
- Scroll-to-bottom enforcement before acceptance
- Explicit acceptance validation
- Timestamp capture for all consent actions
- Device info and IP address logging

 **Consent History**
- Complete consent acceptance records per user
- Consent revocation with timestamp tracking
- Historical version tracking

 **Audit & Compliance**
- Full audit logging for all consent actions
- Supports temporary user_id from Module 2
- Regulatory-compliant data retention

---

## Technology Stack

| Component | Version |
|-----------|---------|
| **Framework** | FastAPI |
| **Server** | Uvicorn |
| **Database** | PostgreSQL (SQLAlchemy ORM) |
| **PDF Generation** | ReportLab |
| **Python** | 3.13+ |
| **Environment Management** | python-dotenv |

### Dependencies

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
reportlab
```

---

## Project Structure

```
lsp_consent_system_3/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration (create locally)
│
└── app/
    ├── main.py                  # FastAPI application entry point
    │
    ├── core/
    │   ├── config.py            # Configuration & environment variables
    │   └── db.py                # Database connection & session management
    │
    ├── models/                  # SQLAlchemy ORM models
    │   ├── consent_master.py    # Master legal document records
    │   ├── user_consent.py      # User consent acceptance records
    │   └── audit_logs.py        # Compliance audit trail
    │
    ├── routers/
    │   ├── crud_routers.py      # Consent CRUD operations
    │   └── legal_routers.py     # Legal document retrieval & PDF downloads
    │
    ├── schemas/
    │   └── schema.py            # Pydantic request/response schemas
    │
    ├── service/
    │   └── services.py          # Business logic for consent operations
    │
    ├── consent/
    │   ├── pdf_utils.py         # PDF generation utilities
    │   └── seed.py              # Database seeding for initial documents
    │
    └── __pycache__/             # Python cache files (auto-generated)
```

---

## Database Schema

### 1. **consent_master**
Stores master copies of all legal documents.

| Column | Type | Description |
|--------|-------|------------|
| `id` | Integer |  Primary key |
| `type` | String | Document type (e.g., "Terms & Conditions") |
| `version` | String | Version identifier (e.g., "v1.0") |
| `content` | Text | Full document content |
| `active` | Boolean | Active status (default: True) |
| `created_at` | DateTime | Timestamp of creation |

### 2. **user_consent**
Stores individual user acceptance records.

| Column | Type | Description |
|--------|------|----------|-------------|
| `id` | Integer |  Primary key |
| `user_id` | Integer |  Reference to Module 2 user |
| `consent_type` | String |  Document type accepted |
| `version` | String |  Version accepted |
| `accepted` | Boolean | Acceptance status |
| `scroll_completed` | Boolean | Scroll validation flag |
| `device_info` | String | Device details (user agent) |
| `ip_address` | String | IP address of acceptor |
| `accepted_at` | DateTime | Acceptance timestamp |
| `revoked_at` | DateTime | Revocation timestamp (if revoked) |

### 3. **audit_logs**
Tracks every consent action for compliance.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer |  Primary key |
| `action` | String | Action type (e.g., "CONSENT_ACCEPTED", "CONSENT_REVOKED") |
| `user_id` | Integer | User performing action |
| `details` | String | Additional details (document type & version) |
| `created_at` | DateTime | Timestamp of action |

### Legal Documents Auto-Seeded at Startup

-  Data Consent
-  Terms & Conditions
-  Privacy Policy
-  Credit Bureau Consent

---

## Setup & Installation

### 1. Prerequisites

- Python 3.13+
- PostgreSQL database
- Virtual environment (recommended)

### 2. Clone & Environment Setup

```bash
# Navigate to project directory
cd lsp_consent_system_3

# Create virtual environment
python -m venv MYVENV

# Activate virtual environment
# On Windows:
MYVENV\Scripts\activate

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/lsp_consent_db

# Application Environment
APP_ENV=development

# Consent Version (optional)
DEFAULT_CONSENT_VERSION=v1.0
```

### 5. Initialize Database

Create the PostgreSQL database and tables:

```bash
# Option 1: Using FastAPI startup (tables created automatically on first run)
# Database tables are auto-created when the app starts (see main.py)

# Option 2: Manual database creation
psql -U postgres -c "CREATE DATABASE lsp_consent_db;"
```

---

## API Endpoints

### Legal Documents (Text & PDF)

#### Get Document Text

```http
GET /api/v1/legal/terms
GET /api/v1/legal/privacy-policy
GET /api/v1/legal/data-consent
GET /api/v1/legal/credit-bureau
```

**Response:**
```json
{
  "type": "Terms & Conditions",
  "version": "v1.0",
  "content": "Full document text..."
}
```

#### Download Documents as PDF

```http
GET /api/v1/legal/terms/pdf
GET /api/v1/legal/privacy-policy/pdf
GET /api/v1/legal/data-consent/pdf
GET /api/v1/legal/credit-bureau/pdf
```

---

### Consent Operations

#### Record Consent Acceptance

```http
POST /api/v1/consent/record
```

**Request Body:**
```json
{
  "user_id": 123,
  "consent_type": "Terms & Conditions",
  "version": "v1.0",
  "accepted": true,
  "scroll_completed": true,
  "device_info": "Mozilla/5.0...",
  "ip_address": "192.168.1.1"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Consent recorded successfully."
}
```

#### Get Consent History

```http
GET /api/v1/consent/history?user_id=123
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 123,
    "consent_type": "Terms & Conditions",
    "version": "v1.0",
    "accepted": true,
    "scroll_completed": true,
    "device_info": "...",
    "ip_address": "192.168.1.1",
    "accepted_at": "2026-02-16T10:30:00",
    "revoked_at": null
  }
]
```

#### Revoke Consent

```http
POST /api/v1/consent/revoke
```

**Request Body:**
```json
{
  "user_id": 123,
  "consent_type": "Terms & Conditions"
}
```

**Response:**
```json
{
  "message": "revoked"
}
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL`  | - | PostgreSQL connection string |
| `APP_ENV` | `development` | Application environment |
| `DEFAULT_CONSENT_VERSION` | `v1.0` | Default consent version |

### Security Considerations

- Store `.env` file securely; never commit to version control
- Use strong database credentials in production
- Implement API authentication/authorization at a higher level (API Gateway)
- Validate IP addresses and device information for audit compliance

---

## Running the Application

### Development Mode (with auto-reload)

```bash
# Ensure virtual environment is activated
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Production Mode

```bash
# Run with multiple workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Development

### Project Initialization Flow

1. **Startup Event** (`@app.on_event("startup")`):
   - Database tables are created if they don't exist
   - Legal documents are seeded into `consent_master` table

2. **API Ready**:
   - All endpoints are available for consent collection and document retrieval

### Key Service Functions

**[services.py](app/service/services.py)**:

- `record_consent()` - Save user consent with audit logging
- `revoke_consent()` - Revoke previously accepted consent
- `log()` - Create audit trail entries
- `get_latest_by_type()` - Fetch active document version

### Adding New Consent Types

1. Update document seeding in [seed.py](app/consent/seed.py)
2. Add new endpoints in [legal_routers.py](app/routers/legal_routers.py)
3. Ensure validation in [crud_routers.py](app/routers/crud_routers.py)

---

## Integration with Module 2

This module expects `user_id` from Module 2:
- User identification is handled by the parent LSP system
- Module 3 receives `user_id` in all consent requests
- Maintains full audit trails linking back to Module 2 users

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `DATABASE_URL missing in .env` | Create `.env` file with valid PostgreSQL connection string |
| `Connection refused` | Ensure PostgreSQL is running and credentials are correct |
| Documents not seeding | Check `seed.py` execution; verify database permissions |
| PDF generation fails | Ensure ReportLab is installed: `pip install reportlab` |

---

## License

Part of the Loan Service Platform (LSP) - Levitica Project

---

## Support & Maintenance

For issues or feature requests, contact the LSP development team.

