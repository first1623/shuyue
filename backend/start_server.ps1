$env:DATABASE_URL = "sqlite:///./data/knowledge_graph.db"
Set-Location "c:\Users\zhaoy\CodeBuddy\backend"
Start-Process -FilePath "C:\Users\zhaoy\AppData\Local\Programs\Python\Python313\python.exe" -ArgumentList "minimal_server.py" -WindowStyle Hidden
