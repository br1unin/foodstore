# PROMPT — GENERAR UN NUEVO ECOMMERCE DE COMIDA BASADO EN UNA ARQUITECTURA EXISTENTE (SIN COPIAR CÓDIGO)

## Contexto

Voy a proporcionarte un proyecto completo de ecommerce de comida rápida ya desarrollado (frontend y backend).

Tu objetivo NO es copiar el código ni replicar archivos existentes.

Debes utilizar dicho proyecto únicamente como referencia arquitectónica, funcional y de organización para diseñar y desarrollar un nuevo sistema equivalente desde cero.

Todo el código generado debe ser completamente original.

No debes reutilizar:

* nombres de clases
* nombres de funciones
* nombres de variables
* nombres de componentes
* nombres de archivos
* nombres de carpetas
* consultas SQL
* endpoints exactos
* implementaciones específicas

Debes comprender los conceptos, patrones y arquitectura utilizados y recrearlos mediante una implementación nueva y propia.

---

# Objetivo General

Desarrollar un sistema web full-stack para gestión de pedidos de comida rápida que permita:

### Clientes

* Registrarse
* Iniciar sesión
* Gestionar direcciones
* Explorar catálogo
* Filtrar productos
* Agregar productos al carrito
* Personalizar pedidos
* Realizar pagos
* Consultar historial
* Seguir pedidos en tiempo real

### Administradores

* Gestionar usuarios
* Gestionar productos
* Gestionar categorías
* Gestionar stock
* Gestionar pedidos
* Consultar métricas
* Administrar imágenes
* Supervisar operaciones

### Sistema

* Autenticación segura
* Gestión de roles
* Auditoría de cambios
* Persistencia transaccional
* Actualización en tiempo real
* Gestión de imágenes CDN
* Integración con pasarela de pagos
* API REST documentada
* Arquitectura escalable y mantenible

---

# Stack Tecnológico Obligatorio

## Frontend

* React 18+
* TypeScript
* Vite
* Tailwind CSS
* TanStack Query
* Zustand
* Axios
* React Router
* Recharts

## Backend

* FastAPI
* SQLModel
* PostgreSQL
* WebSockets nativos
* JWT
* Passlib + bcrypt
* Alembic
* Pydantic v2

## Servicios externos

* Cloudinary para imágenes
* MercadoPago para pagos

---

# Arquitectura Backend

Implementar arquitectura por capas estricta.

## Flujo obligatorio

Router
→ Service
→ Unit Of Work
→ Repository
→ Model

Nunca invertir dependencias.

### Router

Responsabilidades:

* recibir requests
* validar DTOs
* delegar al Service
* devolver responses

No debe contener lógica de negocio.

---

### Service

Responsabilidades:

* lógica de negocio
* validaciones
* reglas del dominio
* coordinación de repositorios

Los servicios deben ser stateless.

---

### Unit Of Work

Responsabilidades:

* apertura de sesión
* commit
* rollback
* control transaccional

Ningún Service debe ejecutar commit directamente.

---

### Repository

Responsabilidades:

* acceso a base de datos
* queries
* persistencia

No debe contener reglas de negocio.

---

### Model

Responsabilidades:

* entidades
* relaciones
* constraints

No debe depender de ninguna capa superior.

---

# Arquitectura Frontend

Aplicar Feature-Sliced Design.

## Estructura

pages/
features/
components/
hooks/
store/
api/
types/

Los módulos deben estar desacoplados.

Evitar cross-imports innecesarios.

---

# Gestión de Estado

## Zustand

Crear stores separados para:

### Auth Store

* sesión
* usuario actual
* autenticación

### Cart Store

* carrito
* cantidades
* personalizaciones

### Payment Store

* proceso de pago

### UI Store

* estados visuales globales

### WebSocket Store

* conexión
* reconexión
* eventos recibidos

Persistir únicamente lo necesario.

---

# Gestión de Datos Remotos

Usar exclusivamente TanStack Query para:

* productos
* categorías
* pedidos
* estadísticas
* usuarios

Implementar:

* cache
* invalidaciones
* optimistic updates
* sincronización automática

---

# Módulos del Sistema

## Autenticación

Funciones:

* registro
* login
* refresh token
* logout
* perfil actual

Características:

* JWT Access Token
* Refresh Token
* invalidación de refresh
* hash bcrypt

---

## Usuarios

Funciones:

* CRUD
* asignación de roles
* soft delete

---

## Direcciones

Funciones:

* CRUD completo
* dirección principal

Cada usuario puede tener múltiples direcciones.

---

## Categorías

Funciones:

* CRUD
* jerarquías
* categorías padre/hija
* imágenes

---

## Productos

Funciones:

* CRUD
* stock
* disponibilidad
* múltiples imágenes
* ingredientes
* unidades de medida

Cada producto puede pertenecer a múltiples categorías.

---

## Ingredientes

Características:

* nombre
* stock
* indicador de alérgeno

Permitir ingredientes removibles.

---

## Pedidos

Dominio central del sistema.

Debe incluir:

* creación
* seguimiento
* historial
* cancelación
* trazabilidad completa

---

## Pagos

Integrar MercadoPago.

Características:

* tokenización
* webhook
* idempotencia
* seguimiento de estados

---

## Uploads

Integración con Cloudinary.

Funciones:

* subir imágenes
* eliminar imágenes
* obtener URLs seguras

---

## Estadísticas

Dashboard administrativo con KPIs.

---

# Modelo de Datos

Diseñar un esquema relacional normalizado.

Debe incluir:

## Usuarios

* usuario
* rol
* usuario_rol
* dirección

## Catálogo

* producto
* categoría
* ingrediente
* unidad_medida

## Ventas

* pedido
* detalle_pedido
* historial_estado
* pago

Implementar relaciones N:M donde corresponda.

---

# Soft Delete

Las entidades de negocio deben soportar eliminación lógica mediante:

deleted_at

Nunca eliminar físicamente:

* usuarios
* productos
* categorías

---

# Snapshot Pattern

Al crear un pedido almacenar:

* nombre del producto
* precio del producto
* subtotal

Los datos deben permanecer inmutables aunque el producto cambie posteriormente.

---

# Audit Trail

Mantener historial completo de cambios de estado.

Características:

* append-only
* sin updates
* sin deletes

---

# Máquina de Estados de Pedido

Estados:

1. PENDIENTE
2. CONFIRMADO
3. EN_PREPARACION
4. ENTREGADO
5. CANCELADO

Reglas:

* estados terminales no admiten transiciones
* validar todas las transiciones desde la capa Service
* registrar historial obligatorio

---

# WebSockets

Implementar actualizaciones en tiempo real.

## Eventos

* pedido creado
* pedido confirmado
* pedido en preparación
* pedido entregado
* pedido cancelado
* pago aprobado

## Requisitos

* reconexión automática
* canales administrativos
* canales por pedido
* sincronización con React Query

El broadcast debe ejecutarse únicamente después de una transacción exitosa.

---

# Cloudinary

Implementar:

## Subida

* validación MIME
* tamaño máximo configurable
* URLs seguras

## Eliminación

* mediante identificador único

## Optimización

* WebP automático
* resize
* crop

---

# MercadoPago

Implementar:

## Checkout

* tarjeta
* saldo en cuenta
* medios alternativos

## Seguridad

* tokenización
* webhook
* idempotency key

Nunca almacenar datos sensibles de tarjetas.

---

# Seguridad

Implementar:

## JWT

* access token
* refresh token

## RBAC

Roles:

* ADMIN
* STOCK
* PEDIDOS
* CLIENTE

## Rate Limiting

Login y registro:

* máximo 5 intentos fallidos
* ventana de 15 minutos

## CORS

Configuración correcta frontend/backend.

---

# API REST

Buenas prácticas:

* versionado /api/v1
* respuestas tipadas
* códigos HTTP correctos
* paginación
* filtros
* búsqueda

Errores estandarizados.

---

# Dashboard Administrativo

Implementar:

## KPIs

* ventas del día
* ventas del mes
* ticket promedio
* pedidos activos

## Gráficos

* ventas por período
* productos más vendidos
* pedidos por estado
* ingresos por método de pago

Usar Recharts.

---

# Testing

Implementar pruebas de integración para:

## Auth

* login
* registro
* refresh
* logout

## Pedidos

* creación
* transiciones válidas
* transiciones inválidas

## Estadísticas

* KPIs
* ingresos
* exclusión de pedidos cancelados

## WebSockets

* conexión
* broadcast
* reconexión

Objetivo mínimo:

60% de cobertura.

---

# Calidad de Código

Requisitos obligatorios:

* TypeScript strict
* tipado fuerte
* SOLID
* SRP
* separación de responsabilidades
* funciones pequeñas
* código documentado
* README completo
* estructura escalable

---

# Entregables Esperados

Generar:

1. Arquitectura completa
2. Árbol de carpetas frontend
3. Árbol de carpetas backend
4. Modelo de datos
5. ERD textual
6. Endpoints REST
7. Eventos WebSocket
8. DTOs principales
9. Stores Zustand
10. Query Keys TanStack Query
11. Estrategia de testing
12. Configuración de variables de entorno
13. Plan de implementación paso a paso
14. Código completamente original

IMPORTANTE:

Analiza el proyecto recibido para comprender patrones, organización y decisiones arquitectónicas.

NO copies código.

NO reproduzcas archivos literalmente.

NO reutilices nombres internos.

Diseña una solución nueva inspirada en las mismas buenas prácticas y objetivos funcionales.
