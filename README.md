# Invoice Manager ⚙️📄

**Invoice Manager** es una herramienta para automatizar la descarga, normalización y almacenamiento de CFDI desde Gmail, con persistencia en SQLite y exportación a Excel. 

---

## Características ✨
- Autenticación con Gmail (OAuth)
- Descarga y parseo de archivos XML de facturas
- Conversión XML → JSON
- Persistencia en base de datos (SQLite por defecto)
- Exportación de reportes en Excel (.xlsx)

## Requisitos 🔧
- Python 3.10+
- Dependencias listadas en `requirements.txt`

## Instalación 🚀
```bash
# clonar el repositorio
git clone <https://github.com/DanielRdz4/Invoice_manager>
cd Invoice_manager

# crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate

# instalar dependencias
pip install -r requirements.txt
```

## Configuración 🔐

1. Credenciales de Google
   - Habilita la API de Gmail en tu proyecto en Google Cloud Console (APIs & Services → Library → Gmail API).
   - Crea credenciales OAuth 2.0 (Credentials → Create Credentials → OAuth Client ID). Para este proyecto recomendamos **tipo: Desktop** (o "Other"). Descarga el JSON de credenciales.
   - Coloca el JSON en `~/.secrets/credentials.json` o define la variable de entorno apuntando al archivo:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.secrets/credentials.json"
     ```
   - **Seguridad:** protege el archivo con permisos restrictivos (por ejemplo `chmod 600 ~/.secrets/credentials.json`) y no lo subas al repositorio. El token de acceso (`~/.secrets/gmail_token.json`) se generará en la primera ejecución y también debe mantenerse privado.
   - Nota: si vas a permitir uso por usuarios externos, revisa el proceso de verificación de OAuth de Google (OAuth consent screen). Para uso personal/desarrollo no es necesario publicar la app.
   - Importante: las cuentas personales requieren OAuth interactivo; los *service accounts* no sirven para acceder a Gmail de usuarios individuales sin domain-wide delegation.

2. Configuración de usuario
   - En la primera ejecución se pedirá el `sender_email` y se almacenará en `src/data/user_config.json` (ejemplo):
     ```json
     {
       "sender_email": "tu_email@ejemplo.com"
     }
     ```
   - `sender_email` se usa para construir consultas en Gmail y filtrar mensajes.

### Pasos rápidos de verificación ✅
- Verificar que `.gitignore` incluye `credentials.json`, `gmail_token.json`, `.secrets/`, `raw_data/` y `*.db`.
- Ejecutar el pipeline y confirmar que se abre el navegador para autorizar y que `~/.secrets/gmail_token.json` se genera correctamente.
- Si compartes el repo públicamente: revoca/rota credenciales anteriores en Google Cloud y no subir nunca los JSON al repo.


## Uso ▶️
Ejecuta el pipeline principal:

python -m src.app.main
```
Esto hará:
- Autenticar con Gmail
- Obtener adjuntos XML de mensajes filtrados
- Convertir XML a JSON y guardarlos
- Guardar facturas en la base de datos
- Exportar un archivo `.xlsx` con el reporte

## Estructura del proyecto 🔍
- `src/app/` — entrypoint y pipeline
- `src/integrations/gmail/` — OAuth y cliente Gmail
- `src/domain/cfdi/` — parser XML → JSON
- `src/persistence/` — DB y repositorios
- `src/reporting/` — exportador Excel
- `src/core/` — configuración y rutas
- `src/data/` — archivos generados durante ejecución

---

## Disclaimer ⚠️

Este proyecto se proporciona **“tal cual” (as-is)** y **no se garantiza mantenimiento, soporte ni actualizaciones futuras**. El autor no asume compromiso alguno de corregir errores, adaptar el código a cambios en APIs externas (como Gmail o Google Cloud), ni de mantener compatibilidad con nuevas versiones de Python o dependencias.

El **uso correcto, seguro y legal del proyecto es responsabilidad exclusiva del usuario**, incluyendo, pero no limitándose a:

- La correcta configuración, protección y rotación de credenciales OAuth.
- El cumplimiento de los términos de servicio de Google, Gmail API y cualquier otro servicio externo utilizado.
- El cumplimiento de la legislación fiscal, de protección de datos y privacidad aplicable (por ejemplo, manejo de CFDI y datos personales).

El autor **no será responsable por pérdidas de datos, accesos no autorizados, uso indebido de información, sanciones legales o fiscales**, ni por cualquier daño directo o indirecto derivado del uso de este software.

Al utilizar, modificar o distribuir este proyecto, aceptas hacerlo **bajo tu propio riesgo**.

---

