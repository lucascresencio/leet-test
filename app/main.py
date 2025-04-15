from fastapi import FastAPI
from sqlalchemy import inspect, text

from app.config.database import engine, Base, get_db
from app.routes import (auth, maintainer, ong, staff, user, attendee,
                        volunteer, project, base, campaign)
from app.dependencies import auth_dev
from app.models.user import UserType, User
from app.models.roles import Role
from app.models.staff import Staff
from app.models.card import Card
from app.services.auth_service import get_password_hash
app = FastAPI(title="Leet Desenvolvimento de Programas de Computador LTDA")

# Função para criar as tabelas
def create_tables():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print(f"Tabelas existentes no banco: {existing_tables}")

    # Criar todas as tabelas definidas nos modelos, se ainda não existirem
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas ou verificadas com sucesso!")

# Evento de inicialização do FastAPI
@app.on_event("startup")
async def startup_event():
    create_tables()


#
# REMOVER A PRIMEIRA FUNÇAO E O STARTUP ANTES DE SUBIR PARA PROD
#

# # Função para limpar e recriar as tabelas
# def reset_and_create_tables():
#
#     try:
#         # Ordem de exclusão: tabelas dependentes primeiro
#         with engine.connect() as connection:
#             # Iniciar uma transação
#             trans = connection.begin()
#             try:
#                 # Dropar tabelas na ordem correta com CASCADE
#                 tables = [
#                     "cards",  # Depende de maintainers
#                     "maintainers",  # Depende de users e ongs
#                     "addresses",
#                     "ongs",  # Depende de users
#                     "users",
#                     "user_types"  # Base para users
#                 ]
#                 for table in tables:
#                     try:
#                         connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
#
#                     except Exception as e:
#
#                         raise
#
#                 # Confirmar a transação
#                 trans.commit()
#             except Exception as e:
#                 # Reverter a transação em caso de erro
#                 trans.rollback()
#                 raise
#
#         # Recriar todas as tabelas
#         Base.metadata.create_all(bind=engine)
#
#     except Exception as e:
#
#         raise
#     Base.metadata.create_all(bind=engine)
#
#
# # Popule as tabelas UserType e Role ao iniciar
# @app.on_event("startup")
# def init_data():
#     db = next(get_db())
#     reset_and_create_tables()  # Limpa e recria as tabelas
#
#     # Insere os tipos de usuário
#     if not db.query(UserType).first():
#         db.add_all([
#             UserType(name="staff"),
#             UserType(name="maintainer"),
#             UserType(name="ong")
#         ])
#         db.commit()
#
#     # Insere os papéis
#     if not db.query(Role).first():
#         db.add_all([
#             Role(name="admin"),
#             Role(name="office")
#         ])
#         db.commit()
#
#     # Cria um admin inicial
#     if not db.query(User).filter(User.username == "admin").first():
#         staff_type = db.query(UserType).filter(UserType.name == "staff").first()
#         admin_role = db.query(Role).filter(Role.name == "admin").first()
#         db_user = User(
#             username="admin",
#             password=get_password_hash("admin123"),
#             user_type_id=staff_type.id
#         )
#         db.add(db_user)
#         db.commit()
#         db_staff = Staff(
#             user_id=db_user.id,
#             role_id=admin_role.id
#         )
#         db.add(db_staff)
#         db.commit()

# Registrar rotas
app.include_router(auth.router)
app.include_router(maintainer.router)
app.include_router(ong.router)
app.include_router(auth_dev.router)
app.include_router(staff.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(attendee.router)
app.include_router(volunteer.router)
app.include_router(base.router)
app.include_router(campaign.router)


@app.get("/")
def read_root():
    return {"message": "Leet Desenvolvimento de Programas de Computador LTDA"}