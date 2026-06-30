# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack food order management system. The `prompt.md` at the root describes the architectural requirements this project implements — read it for domain context before making design decisions.

---

## Backend

Located in `backend/`. Python + FastAPI + SQLModel + PostgreSQL.

### Running

```bash
cd backend
uvicorn app.principal:aplicacion --host 0.0.0.0 --port 8000 --reload
# or
bash ejecutar.sh
```

With Docker:
```bash
cd backend
docker-compose up
```

### Tests

```bash
cd backend
pytest                          # all tests
pytest pruebas/test_ordenes.py  # single file
pytest -k "test_crear_orden"    # single test by name
```

Tests use an isolated SQLite database (not PostgreSQL). The `conftest.py` sets `DATABASE_URL` via env before any import, so import order matters — never reorder imports in test files. Rate limiting is disabled in tests via `limitador.enabled = False`.

### Migrations

```bash
cd backend
alembic revision --autogenerate -m "descripcion"
alembic upgrade head
```

---

## Frontend

Located in `frontend/`. React 18 + TypeScript + Vite + Tailwind.

### Running

```bash
cd frontend
npm install
npm run dev       # dev server on :5173
npm run build     # tsc check + vite build
```

Path alias `@/` maps to `frontend/src/`.

---

## Backend Architecture

Strict layered architecture — dependencies flow in one direction only:

```
Router → Service → GestorTransaccion (Unit of Work) → Repository → SQLModel entities
```

- **Router** (`enrutador.py`): receives requests, validates DTOs, delegates to Service. No business logic.
- **Service** (`servicio.py`): business rules, domain validation, coordinates repositories. Stateless. Never calls `commit` directly.
- **GestorTransaccion** (`persistencia/sesion_trabajo.py`): Unit of Work wrapping the SQLModel `Session`. Commit happens automatically when the FastAPI dependency generator closes (`obtener_gestor`). Routers that need to emit WebSocket events *after* commit call `gestor.confirmar()` explicitly before broadcasting.
- **Repository** (`repositorio.py`): database queries only. No business logic.
- **Entities** (`persistencia/entidades/`): SQLModel table definitions. No dependencies on upper layers.

### Configuration

`app/nucleo/ajustes.py` — pydantic-settings reading from `.env` at the repo root (one level above `backend/`). Key vars: `DATABASE_URL`, `CLAVE_SECRETA`, `ORIGENES_CORS`, `NUBE_CDN`, `TOKEN_MP`.

### Auth & RBAC

- JWT via `python-jose`. Access token (30 min) + refresh token (7 days).
- `obtener_cuenta_activa` dependency resolves the authenticated account from the Bearer token.
- `requerir_perfil(*perfiles)` factory creates authorization dependencies checking role assignment.
- Profiles: `ADMINISTRADOR`, `INVENTARIO`, `DESPACHO`, `COMPRADOR`.
- Seed data created at startup: `admin@foodstore.com` / `Admin1234!` with `ADMINISTRADOR` profile.

### Order State Machine

`app/modulos/ordenes/maquina_estados.py` — pure functions, no side effects:

```
PENDIENTE → CONFIRMADO → EN_PREPARACION → ENTREGADO
         ↘                ↘
          CANCELADO (stock is restored if cancelled from PENDIENTE or CONFIRMADO)
```

`ENTREGADO` and `CANCELADO` are terminal states. All transitions validated in `ServicioOrdenes.cambiar_estado`.

### Snapshot Pattern

When an order is created, `PartidaOrden` captures `titulo_capturado` and `precio_capturado` from the article at that moment. These fields are immutable — product changes after order creation don't affect historical data.

### WebSockets

`app/modulos/tiempo_real/` — `GestorConexiones` singleton (`gestor_conexiones`) maintains active WebSocket connections grouped by logical channel strings (e.g. `"ordenes"`, `"ordenes-{id}"`). Broadcast happens in routers, always *after* a successful transaction commit.

### Rate Limiting

`slowapi` with `limitador` instance. Applied on login and register endpoints. Disabled in tests.

---

## Frontend Architecture

Feature-Sliced Design:

```
src/
  paginas/          # Route-level page components
  funcionalidades/  # Feature modules (catalogo, sesion, ordenes, carrito, pago, perfil, admin)
  componentes/      # Shared UI (ui/, comunes/, disposicion/)
  hooks/            # Shared hooks (useDebounce, useAlmacenLocal, useConexionWS)
  almacenes/        # Zustand stores
  api/              # HTTP client + endpoint functions per domain
  lib/              # TanStack Query client + query key factory + formatters
  tipos/            # TypeScript type definitions per domain
```

### State Management

Five Zustand stores in `almacenes/`:
- `sesionStore` — persisted to localStorage (`fs-sesion`). Holds JWT tokens and account info. `tienePerfil(perfil)` checks role membership.
- `carritoStore` — cart items and customizations.
- `pagoStore` — payment flow state.
- `interfazStore` — global UI state.
- `conexionStore` — WebSocket connection lifecycle.

### Remote Data

All server state via TanStack Query. Query keys are centralized in `lib/clavesConsulta.ts` — always use this factory; never hardcode arrays directly. The Axios client in `api/clienteHttp.ts` injects the Bearer token and handles 401 token refresh automatically.

### WebSocket Hook

`hooks/useConexionWS.ts` — connects/disconnects via `conexionStore` based on a `canal` string. Returns `ultimoEvento` and `estaConectado`. Use this hook in feature components that need real-time updates; invalidate TanStack Query caches in response to received events.

---

## Key Domain Terms (Spanish → English)

| Spanish | English |
|---|---|
| cuenta | user account |
| perfil | role/profile |
| domicilio | address |
| rubro | category |
| articulo | product |
| componente | ingredient |
| orden | order |
| partida | order line item |
| bitacora | audit log / state history |
| cobro | payment/charge |
| gestor | manager / unit of work |
| enrutador | router |
| servicio | service |
| repositorio | repository |
| ajustes | settings/configuration |
| almacen | store (Zustand) |
| claves consulta | query keys (TanStack) |
