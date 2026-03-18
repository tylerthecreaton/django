import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlinecourse_project.settings")

import django

django.setup()

from django.template.loader import get_template

get_template("onlinecourse/course_details_bootstrap.html")
print("template ok")
