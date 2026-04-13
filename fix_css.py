import os
import re

tpl_dir = r"myapp/templates"
for f in os.listdir(tpl_dir):
    if not f.endswith(".html"): continue
    path = os.path.join(tpl_dir, f)
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Replace href="static/css/..." with href="{% static 'css/...' %}"
    new_content = re.sub(r'href="static/([^"]+)"', r'href="{% static \'\1\' %}"', content)
    # Replace src="static/images/..." with src="{% static 'images/...' %}"
    new_content = re.sub(r'src="static/([^"]+)"', r'src="{% static \'\1\' %}"', new_content)

    if new_content != content:
        # ensure load static is there
        if '{% load static %}' not in new_content and '{%load static%}' not in new_content:
            if new_content.startswith('{%extends'):
                parts = new_content.split('%}', 1)
                new_content = parts[0] + '%}\n{% load static %}' + parts[1]
            elif new_content.startswith('{% extends'):
                parts = new_content.split('%}', 1)
                new_content = parts[0] + '%}\n{% load static %}' + parts[1]
            else:
                new_content = '{% load static %}\n' + new_content

        with open(path, "w", encoding="utf-8") as file:
            file.write(new_content)
