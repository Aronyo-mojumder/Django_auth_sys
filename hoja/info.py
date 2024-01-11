# settings.py

# Email Configuration for Outlook
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.office365.com'  # Outlook's SMTP server
EMAIL_HOST_USER = 'aronyom22@outlook.com'  # Your Outlook email address
EMAIL_HOST_PASSWORD = 'dvquprtyvbgyjlcj'  # The generated app password
EMAIL_PORT = 587  # Outlook SMTP port (TLS)

# Additional settings (if needed)
DEFAULT_FROM_EMAIL = 'aronyom22@outlook.com'  # Sender's email address
