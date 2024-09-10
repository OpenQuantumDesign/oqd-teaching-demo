# Python Package Template
[![CI](https://github.com/yhteoh/Python_Package_Template/actions/workflows/CI.yml/badge.svg)](https://github.com/yhteoh/Python_Package_Template/actions/workflows/CI.yml)
![Python](https://img.shields.io/badge/Python-3.10|3.11|3.12-blue)

## Installation 
```bash 
pip install -e .
sudo apt install python3-rpi.gpio   # GPIO library
sudo apt install -y python3-picamera2   # camera library
```
## Documentation
To deploy the documentation locally, implemented with [mkdocs](https://www.mkdocs.org/), run the following commands:
```bash
pip install -e .[docs]
mkdocs serve
```
