DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'classroom',
        'USER': 'sola',  # 'root'
        'PASSWORD': 'rlathfdk',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}
SECRET_KEY = 'django-insecure--t9c6ky@5f!gzc8bz@_y+xz@q)097m$^2n6cu7&dc=l1t^rdf6'
