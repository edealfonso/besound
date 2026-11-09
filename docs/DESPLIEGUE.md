# Despliegue gratis: Render + Neon + Cloudflare R2

Guía para publicar el back-end de besound sin pagar y sin administrar ningún servidor.

## Qué vas a montar

```
Navegador ──► besound.vercel.app (front-end, Vercel)
     │
     ├──► https://besound-api.onrender.com   API Django (Render)
     │          └──► Postgres (Neon)
     │
     └──► https://pub-xxxx.r2.dev/audio/...    audios (Cloudflare R2)
```

| Parte | Servicio | Gratis | Si nadie entra en semanas |
|---|---|---|---|
| Front-end | Vercel | sí | sigue funcionando |
| API | Render | sí, sin tarjeta | se duerme; la primera visita tarda 30–60 s |
| Base de datos | Neon | sí, sin tarjeta | se duerme y se despierta sola al instante |
| Audios | Cloudflare R2 | sí, hasta 10 GB | sigue funcionando |

Ningún servicio se pausa de forma que haya que reactivarlo a mano. Los planes gratuitos pueden cambiar: revisa las condiciones de cada uno.

Necesitarás tener a mano: tu copia de los audios (`media/`) y Docker en tu ordenador.

---

## 1. Base de datos en Neon

1. Entra en [neon.com](https://neon.com) y regístrate (puedes usar tu cuenta de GitHub).
2. **Create project**: nombre `besound`, región **AWS Europe Central 1 (Frankfurt)**, la misma que usaremos en Render.
3. En el panel del proyecto pulsa **Connect**, desactiva **Connection pooling** y copia la cadena de conexión. Tiene esta forma:

   ```
   postgresql://neondb_owner:xxxxx@ep-algo-123456.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   ```

   Guárdala: es tu `DATABASE_URL`.

## 2. Bucket en Cloudflare R2

1. En el panel de Cloudflare: **R2 Object Storage → Create bucket**. Nombre `besound`, ubicación automática. **Create bucket**.
2. Dentro del bucket: **Settings → Public access → R2.dev subdomain → Allow**. Apunta el dominio que aparece, del tipo `pub-xxxxxxxx.r2.dev`: es tu `R2_PUBLIC_DOMAIN` (sin `https://`).
3. Vuelve a **R2 Object Storage → Manage API tokens → Create API token** (o *Create User API token*):
   - Permisos: **Object Read & Write**.
   - Ámbito: **Apply to specific buckets only → besound**.
   - **Create**, y copia los tres valores que salen (solo se muestran una vez):
     - **Access Key ID** → `R2_ACCESS_KEY_ID`
     - **Secret Access Key** → `R2_SECRET_ACCESS_KEY`
     - **Endpoint** del tipo `https://<id de cuenta>.r2.cloudflarestorage.com` → `R2_ENDPOINT_URL`

> El dominio `r2.dev` es perfecto para una demo, pero Cloudflare limita su velocidad. Si algún día tienes dominio propio, puedes conectarlo al bucket (*Settings → Custom Domains*) y cambiar `R2_PUBLIC_DOMAIN`.

## 3. Subir los audios y preparar la base de datos (desde tu ordenador)

En la carpeta del proyecto, crea un archivo `render.env` (no se sube a git) con los valores de los pasos anteriores:

```
DATABASE_URL=postgresql://neondb_owner:xxxxx@ep-algo-123456.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
R2_BUCKET_NAME=besound
R2_ENDPOINT_URL=https://<id de cuenta>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_PUBLIC_DOMAIN=pub-xxxxxxxx.r2.dev
```

Y lanza estos comandos, que usan la imagen de Docker del proyecto pero conectada a Neon y R2:

```bash
# Sube todo media/ al bucket (los audios y los SVG). Si lo repites, no duplica nada
docker compose run --rm --env-from-file render.env web python manage.py upload_media

# Crea las tablas en Neon y tu usuario para el admin
docker compose run --rm --env-from-file render.env web python manage.py createsuperuser

# Rellena los textos de todas las páginas con unos por defecto (luego se editan en el admin)
docker compose run --rm --env-from-file render.env web python manage.py load_default_texts
```

> El plan gratuito de Render no tiene consola, por eso estos pasos se hacen desde tu ordenador.
>
> **¿Tienes una copia de la base de datos antigua?** Restáurala en Neon antes de crear el usuario: `docker run --rm -i postgres:17 psql "<DATABASE_URL>" < copia.sql`. Si no, `load_default_texts` deja todas las páginas con textos y luego los cambias en el admin a tu gusto.

Comprueba en el panel de R2 que aparece la carpeta `audio/` con los archivos.

## 4. La API en Render

1. Entra en [render.com](https://render.com) y regístrate **con tu cuenta de GitHub** (no pide tarjeta).
2. **New → Blueprint**, conecta tu GitHub si te lo pide y elige el repositorio **besound**. Render lee el archivo `render.yaml` del repo y propone crear el servicio `besound-api` (plan *Free*, Frankfurt).
3. Te pedirá los valores que no están en el repo. Pega los de tu `render.env`: `DATABASE_URL`, `R2_BUCKET_NAME`, `R2_ENDPOINT_URL`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` y `R2_PUBLIC_DOMAIN`. La clave secreta de Django se genera sola.
4. **Apply**. La primera vez tarda unos minutos en construir la imagen. Cuando el servicio esté en verde (*Live*), su dirección aparece arriba: `https://besound-api.onrender.com` (o con algún sufijo si ese nombre está cogido).

Comprueba en el navegador:

- `https://besound-api.onrender.com/v1/posts/list` → JSON con enlaces a `pub-xxxxxxxx.r2.dev`
- `https://besound-api.onrender.com/admin/` → el admin (entra con el usuario del paso 3)

No hay que configurar el dominio en ningún sitio: Django usa automáticamente el que le asigna Render.

## 5. Conectar el front-end de Vercel

1. En Vercel: proyecto **besound-front** → *Settings* → *Environment Variables*.
2. Cambia `BACKEND_SERVER` a `https://besound-api.onrender.com/` (**con la barra final**: el front le añade `v1/` detrás).
3. *Deployments* → en el último, **⋯ → Redeploy**.

Abre https://besound.vercel.app: la demo vuelve a funcionar.

---

## Mantenimiento

- **Actualizar:** Render vuelve a desplegar solo cada vez que se mergea algo en `main`.
- **Logs:** en Render, servicio `besound-api` → *Logs*.
- **Copia de la base de datos** (desde tu ordenador; usa la misma versión de Postgres que tu proyecto de Neon):
  ```bash
  docker run --rm postgres:17 pg_dump "<DATABASE_URL>" > besound-$(date +%F).sql
  ```
- **Los audios** quedan en R2; puedes descargarlos desde su panel.

## Problemas frecuentes

| Síntoma | Causa probable |
|---|---|
| La primera visita tarda casi un minuto | Normal: Render estaba dormido. Las siguientes van rápidas |
| Vercel muestra *Connection to database server failed* en la primera visita | Render tardó en despertar más de lo que Vercel espera. Recarga pasado un minuto. Si pasa siempre, revisa en Vercel *Settings → Functions* que *Fluid compute* esté activado (permite esperas más largas) |
| Vercel muestra ese error siempre | `BACKEND_SERVER` mal escrito (¿falta la barra final?) o no has hecho *Redeploy* |
| El despliegue en Render falla al arrancar | Revisa los *Logs*: casi siempre es una variable mal copiada (`DATABASE_URL` completa, con `?sslmode=require`) |
| Los sonidos salen en la lista pero no suenan | `R2_PUBLIC_DOMAIN` mal escrito, o el acceso público `r2.dev` del bucket no está activado (paso 2) |
| Error al subir un sonido desde la web | Permisos del token de R2: tiene que ser *Object Read & Write* sobre el bucket `besound` |
| `Bad Request (400)` | Estás entrando por un dominio distinto al de Render. Añádelo en Render a la variable `DJANGO_ALLOWED_HOSTS` |

## Alternativa: servidor propio

Si algún día tienes una máquina propia (Oracle Cloud, un VPS…), en [DESPLIEGUE-SERVIDOR-PROPIO.md](DESPLIEGUE-SERVIDOR-PROPIO.md) está la guía con Docker Compose y Caddy, preparada para alojar varios proyectos en la misma máquina.
