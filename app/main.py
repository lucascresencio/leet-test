from fastapi import FastAPI
from app.config.database import engine, Base, get_db
from app.routes import auth, maintainer, ong, staff
from app.dependencies import auth_dev
from app.models.user import UserType, User
from app.models.roles import Role
from app.models.staff import Staff
from app.services.auth_service import get_password_hash
app = FastAPI(title="Leet Desenvolvimento de Programas de Computador LTDA")

#
# REMOVER A PRIMEIRA FUNÇAO E O STARTUP ANTES DE SUBIR PARA PROD
#

## Função para limpar e recriar as tabelas
# def reset_and_create_tables():
#     # Remove todas as tabelas existentes
#     Base.metadata.drop_all(bind=engine)
#     # Cria todas as tabelas definidas nos modelos
#     Base.metadata.create_all(bind=engine)
#

## Popule as tabelas UserType e Role ao iniciar
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
#             Role(name="office"),
#             Role(name="volunteer")
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
#             email="admin@example.com",
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

@app.get("/")
def read_root():
    return {"message": "Leet Desenvolvimento de Programas de Computador LTDA"}