from fastapi import FastAPI
from app.config.database import engine, Base
from app.routes import auth, maintainer, ong

app = FastAPI(title="Leet Desenvolvimento de Programas de Computador LTDA")

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

# Registrar rotas
app.include_router(auth.router)
app.include_router(maintainer.router)
app.include_router(ong.router)

@app.get("/")
def read_root():
    return {"message": "Leet Desenvolvimento de Programas de Computador LTDA"}