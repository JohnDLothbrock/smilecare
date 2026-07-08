# SmileCare

![Python](https://img.shields.io/badge/Python-Backend-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Vite](https://img.shields.io/badge/Vite-Build-646CFF)
![Oracle](https://img.shields.io/badge/Oracle-Database-F80000)
![Status](https://img.shields.io/badge/Status-Completed-success)

Full-stack dental clinic management system developed with **FastAPI**, **React**, **Vite**, and **Oracle Database**.

SmileCare centralizes the clinical, administrative, financial, inventory, security, and auditing processes of a dental clinic in a single web application.

The project was developed as the final project for the **SC-504 Lenguajes de Base de Datos** course.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Main Features](#main-features)
- [Application Screenshots](#application-screenshots)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [User Roles and Permissions](#user-roles-and-permissions)
- [Main Business Workflows](#main-business-workflows)
- [Database Design](#database-design)
- [Database Course Requirements](#database-course-requirements)
- [Security](#security)
- [Audit System](#audit-system)
- [Password Recovery](#password-recovery)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Oracle Database Configuration](#oracle-database-configuration)
- [Microsoft Outlook Configuration](#microsoft-outlook-configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Main Application Routes](#main-application-routes)
- [Final Testing Checklist](#final-testing-checklist)
- [Security Notes](#security-notes)
- [Academic Context](#academic-context)
- [Authors](#authors)

---

# Project Overview

SmileCare is a full-stack dental clinic management system designed to manage the complete operational workflow of a clinic.

The application provides centralized management for:

- Patients
- Doctors
- Specialties
- Medical schedules
- Doctor availability
- Appointments
- Consultations
- Treatments
- Surgeries
- Medical history
- Invoices
- Invoice details
- Payments
- Payment methods
- Receipts
- Suppliers
- Medical supplies
- Purchases
- Purchase details
- Inventory stock
- Inventory movements
- Users
- Roles
- Permissions
- Application audit events
- Login and access history
- Password recovery

The system uses a normalized Oracle relational database while exposing workflow-oriented screens that simplify the daily operation of the clinic.

---

# Main Features

## Clinical Management

- Patient registration and maintenance
- Doctor management
- Medical specialty management
- Doctor schedule configuration
- Doctor availability management
- Appointment scheduling
- Complete clinical attention workflow
- Consultation registration
- Treatment application
- Surgery registration
- Patient-centered medical history

## Financial Management

- Invoice creation
- Invoice detail management
- Payment registration
- Multiple payment methods
- Payment receipts
- Invoice cancellation and restoration
- Financial history

## Inventory Management

- Supplier management
- Medical supply management
- Purchase registration
- Purchase details
- Automatic stock updates
- Automatic inventory movement generation
- Manual inventory entries and exits
- Stock adjustments
- Product activation and deactivation
- Inventory movement history

## Security and Administration

- JWT authentication
- Argon2 password hashing
- Role-based access control
- Backend permission enforcement
- Frontend route protection
- Permission-aware navigation menu
- User administration
- Role administration
- Permission administration
- Role-permission assignments

## Audit and Monitoring

- Login history
- Logout history
- Failed login attempts
- Access-denied events
- Password recovery events
- Application change history
- Oracle trigger audit history
- Date-range filtering
- User filtering
- Module filtering
- Action filtering
- Result filtering
- CSV export
- TXT export

## Password Recovery

- Forgot-password workflow
- Recovery by username or email
- Real email delivery through Outlook
- Microsoft Graph integration
- OAuth authorization
- One-time recovery tokens
- Token expiration
- Secure password reset
- Audit trail for recovery events

---

# Application Screenshots

The screenshots below document the main workflows and modules of the final application.

---

## 1. Login

![LoginSmileCare1.png](screenshots/LoginSmileCare1.png)

---

## 2. Main Dashboard

![dashboard1.png](screenshots/dashboard1.png)

![dashboard2.png](screenshots/dashboard2.png)

![dashboard3.png](screenshots/dashboard3.png)

---

## 3. Clinica

### Pacientes:

![pacientes.png](screenshots/pacientes.png)

![pacientes2.png](screenshots/pacientes2.png)

### Doctores:

![doctores.png](screenshots/doctores.png)

![doctores1.png](screenshots/doctores1.png)

### Agenda Médica:

![agendamedica.png](screenshots/agendamedica.png)

### Atención Clínica:

![atencionclinica.png](screenshots/atencionclinica.png)

![atencionclinica1.png](screenshots/atencionclinica1.png)

### Expediente Clínico:

![expedienteclinico.png](screenshots/expedienteclinico.png)

---

## 4. Tratamientos

![tratamientos.png](screenshots/tratamientos.png)

---

## 5. Finanzas

### Caja:

![caja.png](screenshots/caja.png)

![caja2.png](screenshots/caja2.png)

### Facturas:

![facturas.png](screenshots/facturas.png)

### Métodos de Pago:

![metodospago.png](screenshots/metodospago.png)

### Pagos:

![pagos.png](screenshots/pagos.png)

---

## 6. Inventario

### Proveedores:

![Proveedores.png](screenshots/Proveedores.png)

### Insumos:

![insumos.png](screenshots/insumos.png)

### Stock/Inventario:

![stock.png](screenshots/stock.png)

---

## 7. Administración

### Administración de Usuarios y Permisos:

![admin1.png](screenshots/admin1.png)

![admin2.png](screenshots/admin2.png)

![admin3.png](screenshots/admin3.png)

![admin4.png](screenshots/admin4.png)

### Auditoría y accesos / Logs:

![auditoria1.png](screenshots/auditoria1.png)

![auditoria2.png](screenshots/auditoria2.png)

![auditoria3.png](screenshots/auditoria3.png)

---

## 12. Reset de Contraseña

![passwordreset.png](screenshots/passwordreset.png)

---

# Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn
- Oracle Database driver (`oracledb`)
- PyJWT
- Argon2 through `pwdlib`
- Python Dotenv
- MSAL
- Microsoft Graph
- Requests

## Frontend

- React
- Vite
- React Router
- JavaScript
- HTML
- CSS

## Database

- Oracle Database
- Oracle Cloud
- Oracle Wallet
- SQL
- PL/SQL
- Packages
- Procedures
- Functions
- Cursors
- Triggers
- Regular expressions

## Development Tools

- PyCharm
- Oracle SQL Developer
- Git
- GitHub
- Microsoft Entra
- Microsoft Graph

---

# System Architecture

SmileCare follows a layered full-stack architecture.

```text
User
  │
  ▼
React Frontend
  │
  │ HTTPS / REST / JSON
  │ JWT Bearer Token
  ▼
FastAPI Backend
  │
  ├── Authentication and Authorization
  ├── Routes
  ├── Services
  ├── Repositories
  ├── Middleware
  ├── Logging
  └── Audit System
  │
  ▼
Oracle Database
  │
  ├── Tables
  ├── Relationships
  ├── Packages
  ├── Procedures
  ├── Functions
  ├── Cursors
  └── Triggers
```

Password recovery uses an additional external integration:

```text
SmileCare Backend
        │
        ▼
Microsoft Authentication Library
        │
        ▼
Microsoft Identity Platform
        │
        ▼
Microsoft Graph
        │
        ▼
Outlook
        │
        ▼
Password Recovery Email
```

---

# Project Structure

```text
smilecare/
│
├── backend/
│   │
│   ├── core/
│   │   ├── auth_dependencies.py
│   │   ├── exception_handlers.py
│   │   ├── logger.py
│   │   └── security.py
│   │
│   ├── middleware/
│   │   ├── audit_logging.py
│   │   └── request_logging.py
│   │
│   ├── repositories/
│   │   ├── auth_repository.py
│   │   ├── audit_repository.py
│   │   ├── audit_admin_repository.py
│   │   └── ...
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── security_routes.py
│   │   ├── audit_admin_routes.py
│   │   └── ...
│   │
│   ├── scripts/
│   │   └── authorize_outlook.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── audit_service.py
│   │   ├── audit_admin_service.py
│   │   ├── outlook_mail_service.py
│   │   └── ...
│   │
│   ├── .env.example
│   ├── database.py
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── src/
│   │   │
│   │   ├── api/
│   │   │   └── apiClient.js
│   │   │
│   │   ├── auth/
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── ForgotPassword.jsx
│   │   │   ├── ResetPassword.jsx
│   │   │   ├── Pacientes.jsx
│   │   │   ├── Doctores.jsx
│   │   │   ├── AgendaMedica.jsx
│   │   │   ├── AtencionClinica.jsx
│   │   │   ├── ExpedienteClinico.jsx
│   │   │   ├── Caja.jsx
│   │   │   ├── Compras.jsx
│   │   │   ├── InventarioStock.jsx
│   │   │   ├── Admin.jsx
│   │   │   └── AuditoriaAdmin.jsx
│   │   │
│   │   └── App.jsx
│   │
│   └── package.json
│
├── docs/
│   └── screenshots/
│
├── main.py
├── .gitignore
└── README.md
```

---

# User Roles and Permissions

SmileCare uses role-based access control.

The application contains four operational roles.

## ADMIN

Full access to the system.

Main access:

- Clinical modules
- Financial modules
- Inventory modules
- User administration
- Role administration
- Permission administration
- Audit dashboard

## DOCTOR

Access to operational and clinical modules without access to system administration.

Main access:

- Patients
- Doctors
- Medical agenda
- Clinical attention
- Medical records
- Treatments
- Financial workflows
- Inventory workflows

The DOCTOR role does not have access to:

- User administration
- Role administration
- Permission administration
- Audit administration

## INVENTARIO

Access only to inventory-related operations.

Main access:

- Suppliers
- Purchases and supplies
- Inventory stock
- Inventory movements

## RECEPCIONISTA

Access to reception, scheduling, and financial workflows.

Main access:

- Patients
- Medical agenda
- Billing
- Invoices
- Payment methods
- Payments

---

# Main Business Workflows

## Clinical Attention

The clinical workflow combines several database entities into a single operational process.

```text
Appointment
    │
    ▼
Consultation
    │
    ▼
Applied Treatment
    │
    └── Optional Surgery
```

The workflow may perform operations involving:

1. `CITAS`
2. `CONSULTAS`
3. `TRATAMIENTOS_CONSULTA`
4. `CIRUGIAS`

This avoids forcing the user to manage each table through separate disconnected screens.

---

## Billing Workflow

```text
Patient
   │
   ▼
Invoice
   │
   ▼
Invoice Details
   │
   ▼
Payment
   │
   ▼
Receipt
```

Invoices support logical cancellation and restoration.

When an invoice is restored:

- It returns to `PAGADA` if a valid payment exists.
- It returns to `PENDIENTE` if no payment has been applied.

---

## Purchase Workflow

A purchase is processed as a single operational workflow.

```text
Supplier
    │
    ▼
Purchase
    │
    ▼
Purchase Details
    │
    ├── Existing Supply
    │
    └── New Supply
    │
    ▼
Stock Update
    │
    ▼
Inventory Movement
```

The workflow coordinates:

1. Supply creation when necessary
2. Purchase creation
3. Purchase detail creation
4. Stock update
5. Automatic inventory movement creation

---

## Inventory Workflow

The inventory module separates product maintenance from stock operations.

Supported operations include:

- Update product data
- Configure minimum stock
- Configure maximum stock
- Activate products
- Deactivate products
- Manual entries
- Manual exits
- Stock adjustments
- Movement history

Automatic purchase movements are preserved as part of the historical record.

---

# Database Design

The database is designed using a normalized relational model.

The main functional areas are:

## Clinical Domain

- `PACIENTES`
- `ESPECIALIDADES`
- `DOCTORES`
- `CITAS`
- `CONSULTAS`
- `TRATAMIENTOS`
- `TRATAMIENTOS_CONSULTA`
- `HISTORIAL_MEDICO`
- `CIRUGIAS`
- `HORARIOS_DOCTORES`
- `DISPONIBILIDAD_DOCTORES`

## Financial Domain

- `FACTURAS`
- `DETALLE_FACTURA`
- `METODOS_PAGO`
- `PAGOS`
- `COMPROBANTES`

## Inventory Domain

- `PROVEEDORES`
- `INSUMOS`
- `INVENTARIO_STOCK`
- `COMPRAS`
- `DETALLE_COMPRA`
- `MOVIMIENTOS_INVENTARIO`

## Security Domain

- `USUARIOS`
- `ROLES`
- `PERMISOS`
- `ROL_PERMISOS`

## Audit and Recovery Domain

- `AUDITORIA_ACCIONES`
- `AUDITORIA_SISTEMA`
- `HISTORIAL_ACCESOS`
- `PASSWORD_RESET_TOKENS`

---

# Database Course Requirements

The project includes the database programming requirements defined for the course.

## PL/SQL Packages

Five CRUD package groups were implemented:

1. Core
2. Clinical
3. Finance
4. Inventory
5. Security

These packages organize related database operations by business domain.

---

## Cursor Procedures

The project includes multiple procedures using:

```sql
SYS_REFCURSOR
```

Cursor-based procedures are used to return result sets from Oracle for list operations.

The project exceeds the minimum requirement of four procedures using cursors.

---

## Regular Expressions

The project includes twelve regular-expression queries.

Oracle regular-expression features are used for validations and data searches, including:

```sql
REGEXP_LIKE
```

---

## Database Triggers

The project includes six database audit triggers distributed across the three required DML operation types.

### INSERT Triggers

- `TRG_AUD_PACIENTES_INSERT`
- `TRG_AUD_DOCTORES_INSERT`

### UPDATE Triggers

- `TRG_AUD_CITAS_UPDATE`
- `TRG_AUD_FACTURAS_UPDATE`

### DELETE Triggers

- `TRG_AUD_TRATAMIENTOS_CONSULTA_DELETE`
- `TRG_AUD_MOVIMIENTOS_INVENTARIO_DELETE`

The triggers write audit information to:

```text
AUDITORIA_ACCIONES
```

This provides database-level auditing independent of the application audit system.

---

# Security

SmileCare applies security controls at several layers.

## Password Security

Passwords are stored using:

```text
Argon2
```

The application supports migration of legacy passwords to modern Argon2 hashes after a successful login.

Passwords are never returned through the API.

---

## Authentication

After a successful login, the backend generates a signed JWT access token.

The token is sent with protected API requests using:

```text
Authorization: Bearer <token>
```

The frontend stores the authenticated session and automatically includes the token in authorized requests.

---

## Authorization

Authorization is enforced in both layers.

### Backend

The FastAPI backend validates permissions before allowing access to protected endpoints.

### Frontend

The React frontend:

- Hides unauthorized menu options
- Protects direct URLs
- Displays only authorized dashboard cards
- Prevents access to restricted pages

Backend protection remains the authoritative security control.

---

## Password Recovery Security

The password recovery flow includes:

- Neutral responses to avoid exposing whether an account exists
- Cryptographically random recovery tokens
- SHA-256 token hashing
- No raw token storage in Oracle
- Configurable expiration period
- Single-use tokens
- Invalidation of previous active recovery tokens
- Argon2 hashing for the new password
- Audit records for recovery activity

---

# Audit System

SmileCare implements auditing at three levels.

## 1. Oracle Trigger Audit

Table:

```text
AUDITORIA_ACCIONES
```

Records database changes generated directly by Oracle triggers.

Examples:

- Patient insertions
- Doctor insertions
- Appointment updates
- Invoice updates
- Treatment relationship deletions
- Inventory movement deletions

---

## 2. Application Audit

Table:

```text
AUDITORIA_SISTEMA
```

Records application operations such as:

- Create
- Update
- Delete
- Restore
- Reverse
- Change state

Recorded information includes:

- Application user
- Role
- Module
- Entity
- Action
- HTTP method
- Route
- Record identifier
- Result
- HTTP status
- IP address
- Request identifier
- Date and time

---

## 3. Access History

Table:

```text
HISTORIAL_ACCESOS
```

Records security and authentication events such as:

- Successful login
- Failed login
- Denied login
- Logout
- Password reset request
- Password reset completion

---

## Audit Dashboard

The administrator can filter audit information by:

- Start date
- End date
- User
- Module
- Action
- Result

The dashboard includes:

- Successful logins
- Failed logins
- Logouts
- Successful changes
- Denied accesses
- Oracle trigger events

Audit information can be exported as:

```text
CSV
TXT
```

---

# Password Recovery

SmileCare includes a real password recovery workflow using Microsoft Outlook.

```text
Login
  │
  ▼
Forgot Password
  │
  ▼
Username or Email
  │
  ▼
Secure One-Time Token
  │
  ▼
Token Hash Stored in Oracle
  │
  ▼
Microsoft Graph
  │
  ▼
Outlook Recovery Email
  │
  ▼
Reset Password Page
  │
  ▼
New Argon2 Password
```

The raw recovery token only exists in the temporary email link.

Oracle stores only:

```text
SHA-256(token)
```

The link:

- Expires after the configured period
- Can only be used once
- Becomes invalid after a successful password change

---

# Installation

## Requirements

Before running the project, install:

- Python
- Node.js
- npm
- Git
- Oracle Database access
- Oracle Wallet
- A configured Microsoft application for Outlook password recovery

---

## 1. Clone the Repository

```bash
git clone https://github.com/JohnDLothbrock/smilecare.git
cd smilecare
```

---

## 2. Create the Python Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

---

## 3. Install Backend Dependencies

From the project root:

```powershell
pip install -r backend/requirements.txt
```

---

## 4. Create the Backend Environment File

Copy:

```text
backend/.env.example
```

as:

```text
backend/.env
```

Windows PowerShell:

```powershell
Copy-Item backend\.env.example backend\.env
```

Then replace the placeholders with the real local configuration.

Never commit:

```text
backend/.env
```

---

## 5. Install Frontend Dependencies

```powershell
cd frontend
npm install
```

Return to the project root when required:

```powershell
cd ..
```

---

# Environment Variables

The backend uses the following environment variables.

## Oracle Database

```env
ORACLE_USER=your_oracle_username
ORACLE_PASSWORD=your_oracle_password
ORACLE_DSN=your_database_service_name
ORACLE_WALLET_DIR=C:/path/to/your/oracle/wallet
ORACLE_WALLET_PASSWORD=your_wallet_password
```

## JWT Authentication

```env
JWT_SECRET_KEY=replace_with_a_long_random_secret
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=480
```

## Microsoft Graph and Outlook

```env
MICROSOFT_CLIENT_ID=your_microsoft_application_client_id
MICROSOFT_AUTHORITY=https://login.microsoftonline.com/consumers
MICROSOFT_SENDER_EMAIL=your-outlook-account@outlook.com
```

## Password Recovery

```env
FRONTEND_RESET_PASSWORD_URL=http://localhost:5173/reset-password
PASSWORD_RESET_EXPIRE_MINUTES=30
```

Use:

```text
backend/.env.example
```

as the configuration reference.

---

# Oracle Database Configuration

SmileCare connects to Oracle using the Python `oracledb` driver and an Oracle Wallet.

The required configuration includes:

```text
Oracle username
Oracle password
Oracle DSN
Oracle Wallet directory
Oracle Wallet password
```

The wallet directory should remain outside the public repository.

Example:

```env
ORACLE_WALLET_DIR=C:/secure/oracle/Wallet_SmileCare
```

The Oracle schema must contain the required:

- Tables
- Primary keys
- Foreign keys
- Constraints
- Packages
- Procedures
- Functions
- Cursors
- Triggers
- Initial role and permission data

---

# Microsoft Outlook Configuration

Password recovery uses Microsoft Graph with OAuth authorization.

## Microsoft Entra App Registration

Create an application registration with:

```text
Name:
SmileCare Password Recovery
```

Supported account type:

```text
Personal Microsoft accounts
```

Authentication platform:

```text
Mobile and desktop applications
```

Redirect URI:

```text
http://localhost
```

Enable:

```text
Allow public client flows
```

Microsoft Graph delegated permission:

```text
Mail.Send
```

No client secret is required for this local public-client flow.

---

## Authorize Outlook

After configuring the Microsoft application and the environment variables, run:

```powershell
python backend/scripts/authorize_outlook.py
```

A browser window opens for Microsoft authorization.

Sign in with the configured sender account and approve the requested email permission.

After successful authorization, the application creates:

```text
backend/.microsoft_token_cache.bin
```

This file must never be committed to Git.

The application uses the cached Microsoft authorization to send password recovery emails.

---

# Running the Application

## Start the Backend

From the project root:

```powershell
.\.venv\Scripts\activate
python -m uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

---

## Start the Frontend

Open another terminal:

```powershell
cd frontend
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The API includes endpoints for:

- Authentication
- Password recovery
- Patients
- Doctors
- Specialties
- Appointments
- Consultations
- Treatments
- Surgeries
- Medical history
- Doctor schedules
- Doctor availability
- Invoices
- Payments
- Payment methods
- Receipts
- Suppliers
- Supplies
- Purchases
- Stock
- Inventory movements
- Users
- Roles
- Permissions
- Audit administration

---

# Main Application Routes

## Public Routes

```text
/login
/forgot-password
/reset-password
```

## Clinical Routes

```text
/pacientes
/doctores
/agenda-medica
/atencion-clinica
/expediente-clinico
/tratamientos
```

## Financial Routes

```text
/caja
/facturas
/metodos-pago
/pagos
```

## Inventory Routes

```text
/proveedores
/compras
/inventario-stock
```

## Administration Routes

```text
/admin
/admin/auditoria
```

Administrative routes require:

```text
ADMIN_GESTIONAR
```

---

# Final Testing Checklist

Before final delivery, verify the following.

## Authentication

- [ ] Correct credentials allow login
- [ ] Incorrect credentials are rejected
- [ ] Enter key submits the login form
- [ ] Logout closes the session
- [ ] Protected routes reject unauthenticated users

## ADMIN

- [ ] Can access all operational modules
- [ ] Can manage users
- [ ] Can manage roles
- [ ] Can manage permissions
- [ ] Can access the audit dashboard

## DOCTOR

- [ ] Can access authorized operational modules
- [ ] Cannot access administration

## INVENTARIO

- [ ] Can access suppliers
- [ ] Can access purchases
- [ ] Can access stock
- [ ] Cannot access unauthorized modules

## RECEPCIONISTA

- [ ] Can access patients
- [ ] Can access the medical agenda
- [ ] Can access billing and payments
- [ ] Cannot access unauthorized modules

## Clinical Workflow

- [ ] Create or update a patient
- [ ] Schedule an appointment
- [ ] Register a consultation
- [ ] Apply a treatment
- [ ] Register an optional surgery
- [ ] Verify the medical record

## Financial Workflow

- [ ] Create an invoice
- [ ] Add invoice details
- [ ] Register a payment
- [ ] Generate or verify a receipt
- [ ] Cancel an invoice
- [ ] Restore an invoice

## Inventory Workflow

- [ ] Create or select a supplier
- [ ] Register a purchase
- [ ] Add new or existing supplies
- [ ] Verify stock increase
- [ ] Verify automatic inventory movement
- [ ] Test a manual entry
- [ ] Test a manual exit

## Audit

- [ ] Successful login appears in access history
- [ ] Failed login appears in access history
- [ ] Logout appears in access history
- [ ] Application changes appear in the audit dashboard
- [ ] Oracle trigger events appear in the audit dashboard
- [ ] Date filters work
- [ ] CSV export works
- [ ] TXT export works

## Password Recovery

- [ ] Forgot-password link is visible
- [ ] Recovery request returns a neutral message
- [ ] Outlook email is received
- [ ] Recovery link opens the reset page
- [ ] New password is accepted
- [ ] Old password stops working
- [ ] New password allows login
- [ ] Used recovery link cannot be reused
- [ ] Recovery events appear in the audit dashboard

---

# Security Notes

The following files and values must never be committed:

```text
backend/.env
backend/.microsoft_token_cache.bin
Oracle Wallet files
Virtual environments
node_modules
Application logs
Passwords
JWT secrets
Real recovery tokens
```

The repository should contain only:

```text
backend/.env.example
```

with safe placeholder values.

Before pushing changes, verify:

```powershell
git status
```

---

# Academic Context

SmileCare was developed as a university database project for:

```text
Course:
SC-504 Lenguajes de Base de Datos
```

The project demonstrates the integration of:

- Relational database design
- Database normalization
- SQL
- PL/SQL
- CRUD operations
- Packages
- Procedures
- Functions
- Cursors
- Regular expressions
- Database triggers
- Referential integrity
- Oracle auditing
- Full-stack application development
- Authentication
- Authorization
- External service integration

The final result combines database programming requirements with a complete web application connected to Oracle.

---

# Authors

## Developers:

***Juan Andrey Ureña Chaves***


GitHub:

```text
https://github.com/JohnDLothbrock
```

Project repository:

```text
https://github.com/JohnDLothbrock/smilecare
```

---

# Project Status

```text
Database design              ✅ Completed
Oracle integration           ✅ Completed
Backend API                  ✅ Completed
Frontend application         ✅ Completed
Authentication               ✅ Completed
Role-based access control    ✅ Completed
Clinical workflows           ✅ Completed
Financial workflows          ✅ Completed
Inventory workflows          ✅ Completed
Audit dashboard              ✅ Completed
Password recovery            ✅ Completed
Security cleanup             ✅ Completed
README documentation         ✅ Completed
```

---

# License

This project was developed for academic and educational purposes but the app is ready for real life use, encapsulated using Docker.

The source code is publicly available as part of the university project submission.