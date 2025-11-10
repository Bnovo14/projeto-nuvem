# main.py
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
# Importações do SQLModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional

# -------------------------------------------------------------------
# 1. CONFIGURAÇÃO DO BANCO DE DADOS (PostgreSQL)
# -------------------------------------------------------------------

# ATENÇÃO: Substitua pela sua string de conexão do PostgreSQL
# Formato: "postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO"
DATABASE_URL = "postgresql://postgres:sua_senha_aqui@localhost/catalogofilmes"

# Cria a "engine" de conexão.
# O connect_args é recomendado pelo FastAPI/SQLModel para SQLite, mas
# para Postgres, a string de conexão é suficiente.
engine = create_engine(DATABASE_URL)


# Função que cria as tabelas no banco de dados
def create_db_and_tables():
    # SQLModel.metadata.create_all() irá criar as tabelas
    # que herdam de SQLModel e têm table=True
    SQLModel.metadata.create_all(engine)


# -------------------------------------------------------------------
# 2. MODELOS SQLModel (Tabela do BD e Schemas da API)
# -------------------------------------------------------------------

# SQLModel nos permite definir os campos uma única vez.

# Este é o modelo "Base", com os campos que esperamos
# na criação (input da API) e que estão no banco.
class Filme(SQLModel, table=True):
    """Modelo mapeado para a tabela do banco de dados.
    Usamos apenas essa classe para o mapeamento (table=True) para
    evitar múltiplas declarações da mesma tabela.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(index=True)  # Index=True otimiza buscas por título
    diretor: str
    ano: int
    genero: str


# Schema para leitura (response_model)
class FilmeRead(SQLModel):
    id: int
    titulo: str
    diretor: str
    ano: int
    genero: str


# Schema para criação/atualização (input da API)
class FilmeCreate(SQLModel):
    titulo: str
    diretor: str
    ano: int
    genero: str
    
# Este é o modelo de ATUALIZAÇÃO (input da API - opcional mas boa prática).
# Torna todos os campos opcionais para permitir updates parciais (PATCH).
# Para este exemplo simples (PUT), vamos usar FilmeCreate.

# -------------------------------------------------------------------
# 3. INICIALIZAÇÃO E DEPENDÊNCIAS DA API
# -------------------------------------------------------------------

# Criamos o app FastAPI e dizemos para ele chamar a função
# create_db_and_tables() durante a inicialização.
app = FastAPI(
    title="API de Catálogo de Filmes com SQLModel",
    description="Um CRUD simples de filmes em Python com FastAPI e PostgreSQL.",
    on_startup=[create_db_and_tables]  # Cria as tabelas ao iniciar
)

# Função "Dependency" para injetar a sessão do banco em cada rota
# Este é o padrão recomendado pelo SQLModel, usando 'with'
def get_db():
    with Session(engine) as session:
        yield session

# -------------------------------------------------------------------
# 4. ENDPOINTS DO CRUD
# -------------------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Catálogo de Filmes com SQLModel!"}

# --- CREATE (Criar) ---
@app.post("/filmes/", response_model=FilmeRead, status_code=status.HTTP_201_CREATED)
def create_filme(filme: FilmeCreate, db: Session = Depends(get_db)):
    """
    Cria um novo filme no catálogo.
    """
    # Converte o schema FilmeCreate para o modelo de tabela Filme
    # O .model_validate() é a forma moderna (Pydantic v2) de fazer isso
    db_filme = Filme.model_validate(filme)
    
    db.add(db_filme)
    db.commit()
    db.refresh(db_filme)  # Atualiza db_filme com o ID do banco
    
    return db_filme

# --- READ (Ler - Todos) ---
@app.get("/filmes/", response_model=List[FilmeRead])
def read_filmes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os filmes do catálogo, com paginação.
    """
    # No SQLModel, usamos 'select()'
    statement = select(Filme).offset(skip).limit(limit)
    filmes = db.exec(statement).all()
    return filmes

# --- READ (Ler - Um) ---
@app.get("/filmes/{filme_id}", response_model=FilmeRead)
def read_filme(filme_id: int, db: Session = Depends(get_db)):
    """
    Obtém os detalhes de um filme específico pelo seu ID.
    """
    # db.get() é a forma mais rápida de buscar pela Primary Key
    db_filme = db.get(Filme, filme_id)
    
    if not db_filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    return db_filme

# --- UPDATE (Atualizar) ---
@app.put("/filmes/{filme_id}", response_model=FilmeRead)
def update_filme(filme_id: int, filme: FilmeCreate, db: Session = Depends(get_db)):
    """
    Atualiza as informações de um filme existente (substituição total).
    """
    db_filme = db.get(Filme, filme_id)
    
    if not db_filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    # Pega os dados do 'filme' (FilmeCreate) que veio da requisição
    # .model_dump() converte o modelo Pydantic/SQLModel para um dict
    filme_data = filme.model_dump(exclude_unset=True)
    
    # Atualiza os campos do objeto 'db_filme' (que veio do banco)
    for key, value in filme_data.items():
        setattr(db_filme, key, value)
    
    db.add(db_filme)  # Adiciona o objeto modificado à sessão
    db.commit()
    db.refresh(db_filme)  # Atualiza o objeto com os dados do banco
    
    return db_filme

# --- DELETE (Deletar) ---
@app.delete("/filmes/{filme_id}", response_model=FilmeRead)
def delete_filme(filme_id: int, db: Session = Depends(get_db)):
    """
    Remove um filme do catálogo.
    """
    db_filme = db.get(Filme, filme_id)
    
    if not db_filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    db.delete(db_filme)
    db.commit()
    
    # Retorna o objeto que acabou de ser deletado
    # Isso funciona pois a sessão só é fechada pelo 'with' no 'get_db'
    # depois que a resposta é enviada.
    return db_filme

# -------------------------------------------------------------------
# 5. EXECUTAR O SERVIDOR (Apenas para fins de teste local)
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("Iniciando servidor em http://127.0.0.1:8000")
    print("Acesse a documentação da API em http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)