from .development import *

# GENERAL

SECRET_KEY = '*piusv42ywk&=dy$xc$qmk$vch17zo2-kzxi0+d4o($yvy4wv-'

TEST_RUNNER = "django.test.runner.DiscoverRunner"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

TEMPLATES[-1]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# EMAIL

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
