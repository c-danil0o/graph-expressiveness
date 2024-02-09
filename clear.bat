@echo off

REM This script is used to uninstall all installed Python components.

REM Uninstall installed Python components
pip uninstall -y block_visualizer
pip uninstall -y simple_visualizer
pip uninstall -y data_source_ethereum
pip uninstall -y data_source_github

echo All plugins uninstalled successfully.
