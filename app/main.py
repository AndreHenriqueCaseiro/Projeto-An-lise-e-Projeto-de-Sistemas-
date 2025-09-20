# app/main.py

from fastapi import FastAPI
# Esta linha importa a variável 'produtos_router' do arquivo produtos_router.py
from .routers import produtos_router, locais_router, auth_router 

from fastapi import FastAPI
from .routers import produtos_router, locais_router 

app = FastAPI(
    title="API de Gestão de Itens",
    description="API para gerenciar produtos e itens de um estoque.",
    version="1.0.0"
)

# Esta linha usa o que foi importado. Ela espera que 'produtos_router' 
# tenha um objeto chamado 'router' dentro dele.
app.include_router(produtos_router.router)
app.include_router(locais_router.router)
app.include_router(auth_router.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Gestão de Itens!"}