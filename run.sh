#!/bin/bash

# Activar el entorno virtual de Python
source bedrock/bin/activate

# Ejecutar uvicorn en modo detached (en segundo plano)
nohup uvicorn main:app --reload > uvicorn.log 2>&1 &

# Ejecutar Streamlit en modo detached (en segundo plano)
nohup streamlit run streamlit_app.py > streamlit.log 2>&1 &

# Puedes agregar cualquier otro comando o logging aquí