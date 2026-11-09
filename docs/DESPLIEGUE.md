# Despliegue en Oracle Cloud (gratis)

Guía para publicar el back-end de besound en una máquina virtual gratuita de Oracle Cloud, con HTTPS y sin comprar dominio. La misma máquina sirve para alojar más proyectos después.

## Qué vas a montar

```
Navegador ──► besound.vercel.app (front-end, Vercel)
     │
     └──► https://besound.<IP>.sslip.io
              │
        ┌─────▼──────────── máquina de Oracle ───────────────────┐
        │  Caddy (puertos 80/443, certificados HTTPS automáticos) │
        │     ├──► besound: nginx ─► Django (gunicorn) ─► Postgres │
        │     └──► (más proyectos en el futuro)                    │
        └──────────────────────────────────────────────────────────┘
```

- **Caddy** es la única puerta de entrada: recibe todo el tráfico, consigue los certificados HTTPS de Let's Encrypt y reparte cada petición al proyecto que toca según el nombre.
- **sslip.io** convierte la IP de la máquina en un nombre de dominio gratis: `besound.132-145-10-20.sslip.io` apunta a `132.145.10.20`. No hay que registrarse ni configurar nada.

En toda la guía, cambia `132.145.10.20` / `132-145-10-20` por la IP de tu máquina.

---

## 1. Crear la máquina

1. Crea una cuenta en [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/). Piden tarjeta para verificar, pero las máquinas «Always Free» no se cobran.
2. Menú → **Compute → Instances → Create instance**.
3. **Image:** Canonical Ubuntu 24.04.
4. **Shape:** *Ampere* → `VM.Standard.A1.Flex` (tiene la etiqueta *Always Free eligible*). Con 1–2 OCPU y 6–12 GB de memoria vas sobrada.
5. **SSH keys:** elige *Generate a key pair* y descarga la clave privada (por ejemplo `oracle.key`), o sube tu clave pública si ya tienes una.
6. **Networking:** deja que cree la red y marca *Assign a public IPv4 address*.
7. Pulsa **Create** y apunta la **IP pública** cuando la máquina esté en verde.

> Si sale *Out of capacity*, prueba otro *Availability domain* o vuelve a intentarlo más tarde: pasa a menudo con las máquinas gratuitas.

## 2. Abrir los puertos 80 y 443

Hay que abrirlos en **dos sitios** (el olvido más típico es el segundo):

**a) En Oracle:** en la página de la instancia → enlace de la *Subnet* → *Security Lists* → *Default Security List* → **Add Ingress Rules**:

| Source CIDR | IP Protocol | Destination Port |
|---|---|---|
| `0.0.0.0/0` | TCP | `80` |
| `0.0.0.0/0` | TCP | `443` |

**b) En Ubuntu:** las imágenes de Oracle traen un cortafuegos propio. Entra en la máquina desde tu ordenador:

```bash
chmod 600 ~/Downloads/oracle.key
ssh -i ~/Downloads/oracle.key ubuntu@132.145.10.20
```

y ya dentro:

```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```

## 3. Instalar Docker

```bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
exit
```

Vuelve a entrar con `ssh` (para que se aplique el grupo `docker`) y comprueba que funciona con `docker run --rm hello-world`.

## 4. Caddy (una sola vez por máquina)

```bash
docker network create web
sudo mkdir -p /srv/caddy && sudo chown ubuntu: /srv/caddy && cd /srv/caddy
```

Crea `/srv/caddy/docker-compose.yml`:

```yaml
services:
  caddy:
    image: caddy:2
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "443:443/udp"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    networks:
      - web

volumes:
  caddy_data:
  caddy_config:

networks:
  web:
    external: true
```

Y `/srv/caddy/Caddyfile`, con un bloque por proyecto:

```
besound.132-145-10-20.sslip.io {
    reverse_proxy besound:80
}
```

Todavía no lo arranques: primero besound (paso 5), si no Caddy no encuentra a quién enviar las peticiones.

## 5. besound

### Descargar el código y configurar

```bash
sudo mkdir -p /srv/besound && sudo chown ubuntu: /srv/besound
git clone https://github.com/edealfonso/besound.git /srv/besound
cd /srv/besound
cp .env.example .env
```

Edita `.env` (`nano .env`):

```
DJANGO_SECRET_KEY=           # genera una con: openssl rand -hex 32
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=besound.132-145-10-20.sslip.io
DJANGO_CSRF_TRUSTED_ORIGINS=https://besound.132-145-10-20.sslip.io

POSTGRES_DB=besound
POSTGRES_USER=besound
POSTGRES_PASSWORD=           # genera otra con: openssl rand -hex 16
```

### Subir los audios

Desde **tu ordenador** (en la carpeta del proyecto, donde está tu copia de los audios):

```bash
ssh -i ~/Downloads/oracle.key ubuntu@132.145.10.20 mkdir -p /srv/besound/media
rsync -avz -e "ssh -i ~/Downloads/oracle.key" media/ ubuntu@132.145.10.20:/srv/besound/media/
```

### Arrancar

De vuelta en la máquina:

```bash
cd /srv/besound
docker compose -f docker-compose.yml -f docker-compose.server.yml up -d --build
docker compose exec web python manage.py createsuperuser
```

`docker-compose.server.yml` añade lo que hace falta en el servidor: reinicio automático, ningún puerto público (solo se entra por Caddy) y la conexión a la red `web` con el nombre `besound`.

> **¿Tienes una copia de la base de datos antigua?** Restáurala antes del primer arranque completo: `docker compose up -d db`, luego `docker compose exec -T db psql -U besound besound < copia.sql`, y después el `up -d --build` de arriba (las migraciones se aplican solas). Si no la tienes, rellena los textos de las páginas desde el admin.

### Encender Caddy

```bash
cd /srv/caddy
docker compose up -d
docker compose logs -f     # espera a ver "certificate obtained successfully", luego Ctrl+C
```

Comprueba en el navegador:

- https://besound.132-145-10-20.sslip.io/v1/home → devuelve JSON
- https://besound.132-145-10-20.sslip.io/admin/ → el admin, con candado HTTPS

## 6. Conectar el front-end de Vercel

1. En Vercel: proyecto **besound-front** → *Settings* → *Environment Variables*.
2. Cambia `BACKEND_SERVER` a `https://besound.132-145-10-20.sslip.io/` (**con la barra final**: el front le añade `v1/` detrás).
3. *Deployments* → en el último, **⋯ → Redeploy**.

Abre https://besound.vercel.app: la demo vuelve a funcionar. Si el front estuviera en otro dominio, añádelo en el `.env` de besound con `CORS_ALLOWED_ORIGINS=https://besound.vercel.app,https://otro-dominio`.

---

## Añadir otro proyecto a la misma máquina

1. En el `docker-compose` del proyecto, conecta su servidor web a la red `web` con un nombre propio, igual que hace `docker-compose.server.yml` con `besound`:
   ```yaml
   networks:
     default:
     web:
       aliases: [miproyecto]
   ```
   y sin publicar puertos.
2. Añade un bloque al `Caddyfile`:
   ```
   miproyecto.132-145-10-20.sslip.io {
       reverse_proxy miproyecto:80
   }
   ```
3. Recarga Caddy: `cd /srv/caddy && docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile`.

## Mantenimiento

**Actualizar besound** después de mergear cambios en GitHub:

```bash
cd /srv/besound && git pull
docker compose -f docker-compose.yml -f docker-compose.server.yml up -d --build
```

**Copias de seguridad.** Oracle puede recuperar máquinas gratuitas que llevan mucho tiempo sin uso, así que guarda copias fuera de la máquina. Desde tu ordenador:

```bash
ssh -i ~/Downloads/oracle.key ubuntu@132.145.10.20 \
  "cd /srv/besound && docker compose exec -T db pg_dump -U besound besound" > besound-$(date +%F).sql
rsync -avz -e "ssh -i ~/Downloads/oracle.key" ubuntu@132.145.10.20:/srv/besound/media/ media/
```

**Ver qué pasa:** `docker compose logs -f web` (en `/srv/besound`) o `docker compose logs -f` (en `/srv/caddy`).

## Pasar a un dominio propio

Si más adelante compras un dominio (por ejemplo `elsadealfonso.es`):

1. En el panel del dominio, crea un registro **A**: `besound` → `132.145.10.20`.
2. En el `Caddyfile`, cambia `besound.132-145-10-20.sslip.io` por `besound.elsadealfonso.es` y recarga Caddy.
3. En `/srv/besound/.env`, cambia `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS`, y vuelve a lanzar el `up -d`.
4. En Vercel, cambia `BACKEND_SERVER` y haz *Redeploy*.

## Problemas frecuentes

| Síntoma | Causa probable |
|---|---|
| La página no carga (timeout) | Faltan los puertos 80/443 en Oracle **o** en `iptables` (paso 2) |
| Caddy no consigue el certificado | Lo mismo: Let's Encrypt necesita llegar al puerto 80/443. Si el error menciona *rate limit*, usa `nip.io` en vez de `sslip.io` (funciona igual: `besound.132-145-10-20.nip.io`) |
| `Bad Request (400)` | El nombre no está en `DJANGO_ALLOWED_HOSTS` del `.env` |
| `502 Bad Gateway` | besound aún está arrancando (espera unos segundos) o no está en la red `web`: revisa que lo arrancaste con `-f docker-compose.server.yml` |
| Error CSRF al entrar al admin | `DJANGO_CSRF_TRUSTED_ORIGINS` debe ser exactamente `https://` + el nombre |
| La web de Vercel dice *Connection to database server failed* | `BACKEND_SERVER` mal escrito (¿falta la barra final?) o no has hecho *Redeploy* |
