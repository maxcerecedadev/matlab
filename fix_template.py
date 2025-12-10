#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para corregir el error de sintaxis en misiones.html"""

import re

file_path = r"C:\Users\Alex\Desktop\Project\matelab\templates\dashboards\misiones.html"

# Leer el archivo
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar las líneas malformadas
# Patrón 1: Corregir el encabezado
old_header = r"{% extends 'layout/master\.html' %} {% load custom_filters %} {% block title\n%}Misiones{% endblock %} {% block layout %}"
new_header = """{% extends 'layout/master.html' %}
{% load custom_filters %}

{% block title %}Misiones{% endblock %}

{% block layout %}"""

content = re.sub(old_header, new_header, content)

# Patrón 2: Corregir los includes del menú
old_menu = r"{% if user\.rol\.tipo == 'Estudiante' %} {% include\n    'layout/partials/menu/vertical/student_menu\.html' %} {% elif user\.rol\.tipo\n    == 'Profesor' %} {% include\n    'layout/partials/menu/vertical/professor_menu\.html' %} {% endif %}"
new_menu = """{% if user.rol.tipo == 'Estudiante' %}
      {% include 'layout/partials/menu/vertical/student_menu.html' %}
    {% elif user.rol.tipo == 'Profesor' %}
      {% include 'layout/partials/menu/vertical/professor_menu.html' %}
    {% endif %}"""

content = re.sub(old_menu, new_menu, content)

# Escribir el archivo corregido
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Archivo corregido exitosamente")
