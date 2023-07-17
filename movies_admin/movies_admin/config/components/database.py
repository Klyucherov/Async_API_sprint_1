from os import environ

DATABASES = {
    'default': {
        'ENGINE': environ.get('DB_ENGINE', "django.db.backends.sqlite3"),
        'NAME': environ.get('DB_NAME', 'db_name'),
        'USER': environ.get('DB_USER', 'user'),
        'PASSWORD': environ.get('DB_PASSWORD', 'password'),
        'HOST': environ.get('DB_HOST', 'localhost'),
        'PORT': environ.get('DB_PORT', 5432),
        'OPTIONS': {
            'options': '-c search_path=public,content',
        },
    },
}
