from .base import *
import os
from urllib.parse import parse_qs, urlparse

DEBUG = False

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-in-production")

def _normalize_allowed_hosts(raw_hosts):
    hosts = []
    for host in raw_hosts.split(","):
        value = host.strip()
        if not value:
            continue
        if "://" in value:
            parsed = urlparse(value)
            value = parsed.netloc or parsed.path
        value = value.split("/")[0]
        if value:
            hosts.append(value)
    return hosts


def _normalize_csrf_origins(raw_origins):
    origins = []
    for origin in raw_origins.split(","):
        value = origin.strip()
        if not value:
            continue
        if "://" not in value:
            value = f"https://{value}"
        parsed = urlparse(value)
        if parsed.scheme and parsed.netloc:
            origins.append(f"{parsed.scheme}://{parsed.netloc}")
    return origins


ALLOWED_HOSTS = _normalize_allowed_hosts(
    os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
)

CSRF_TRUSTED_ORIGINS = _normalize_csrf_origins(
    os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "")
)

if os.environ.get("DJANGO_SECURE_COOKIES", "1") == "1":
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

if os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "0") == "1":
    SECURE_SSL_REDIRECT = True

if os.environ.get("DJANGO_USE_X_FORWARDED_PROTO", "1") == "1":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Prefer managed Postgres when DATABASE_URL is provided.
database_url = os.environ.get("DATABASE_URL", "").strip()
if database_url:
    parsed = urlparse(database_url)
    if parsed.scheme.startswith("postgres"):
        if "django.contrib.postgres" not in INSTALLED_APPS:
            INSTALLED_APPS.append("django.contrib.postgres")
        query = parse_qs(parsed.query)
        DATABASES["default"] = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": (parsed.path or "/")[1:],
            "USER": parsed.username or "",
            "PASSWORD": parsed.password or "",
            "HOST": parsed.hostname or "",
            "PORT": str(parsed.port or "5432"),
            "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),
            "OPTIONS": {},
        }
        sslmode = query.get("sslmode", [""])[0]
        if sslmode:
            DATABASES["default"]["OPTIONS"]["sslmode"] = sslmode
    else:
        raise ValueError("Unsupported DATABASE_URL scheme. Use postgres:// or postgresql://")

# Optional sqlite/media path overrides for disk-backed deployments.
sqlite_path = os.environ.get("SQLITE_PATH", "").strip()
if sqlite_path and not database_url:
    sqlite_dir = os.path.dirname(sqlite_path)
    if sqlite_dir:
        try:
            os.makedirs(sqlite_dir, exist_ok=True)
        except PermissionError:
            # Do not fail hard at import-time; runtime/storage config will surface issues if any.
            pass
    DATABASES["default"]["NAME"] = sqlite_path

media_root = os.environ.get("DJANGO_MEDIA_ROOT", "").strip()
if media_root:
    MEDIA_ROOT = media_root

# Serve static/media from Django when no reverse proxy is present (MVP mode).
SERVE_STATIC_IN_APP = os.environ.get("DJANGO_SERVE_STATIC", "1") == "1"

# Use non-manifest static storage by default for safer MVP deploys.
# Enable manifest mode only when explicitly requested.
if os.environ.get("DJANGO_USE_MANIFEST_STATIC", "0") == "1":
    STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
else:
    STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.StaticFilesStorage"

WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "http://localhost:8000")

try:
    from .local import *
except ImportError:
    pass
