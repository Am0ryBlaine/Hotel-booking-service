#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import locale

os.environ["PYTHONUTF8"] = "1"
os.environ["PGCLIENTENCODING"] = "UTF-8"
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
