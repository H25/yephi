DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4as23-ag5c@gg+&as$asg$x)mp$saQ#gast%bz#&z=@d6tf0oz%g6%gq%!+1$'

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEFAULT_FROM_EMAIL = ''
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
