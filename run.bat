@echo off

REM This script is used to build all necessary python components and run Django website.

REM Install necessary Python components
pip install .\block_visualizer
pip install .\simple_visualizer
pip install .\data_source_ethereum
pip install .\data_source_github

REM Run Django website
@REM cd %1
cd graph_explorer
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

