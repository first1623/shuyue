@echo off
set DATABASE_URL=sqlite:///./data/knowledge_graph.db
cd /d "%~dp0"
C:\Users\zhaoy\AppData\Local\Programs\Python\Python313\python.exe minimal_server.py
