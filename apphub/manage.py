#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    profile = os.environ.setdefault("APPHUB_PROFILE", "dev")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apphub.settings.%s" % profile)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
