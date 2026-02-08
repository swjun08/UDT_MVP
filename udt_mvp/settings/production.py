from .base import *
import os

DEBUG = False

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-in-production")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

if os.environ.get("DJANGO_SECURE_COOKIES", "1") == "1":
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

if os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "0") == "1":
    SECURE_SSL_REDIRECT = True

if os.environ.get("DJANGO_USE_X_FORWARDED_PROTO", "1") == "1":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Optional sqlite/media path overrides for disk-backed deployments.
sqlite_path = os.environ.get("SQLITE_PATH", "").strip()
if sqlite_path:
    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    DATABASES["default"]["NAME"] = sqlite_path

media_root = os.environ.get("DJANGO_MEDIA_ROOT", "").strip()
if media_root:
    os.makedirs(media_root, exist_ok=True)
    MEDIA_ROOT = media_root

# Serve static/media from Django when no reverse proxy is present (MVP mode).
SERVE_STATIC_IN_APP = os.environ.get("DJANGO_SERVE_STATIC", "1") == "1"

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/6.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "http://localhost:8000")

try:
    from .local import *
except ImportError:
    pass
