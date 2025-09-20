# test_day3.py

# ====================================================================
# PARTE 1: TESTANDO AS FUNÇÕES DE SEGURANÇA (SENHAS)
# ====================================================================
print("--- Iniciando Teste de Segurança ---")
from app.security import get_password_hash, verify_password

senha_original = "senha_super_secreta"
hash_da_senha = get_password_hash(senha_original)

print(f"Senha Original: {senha_original}")
print(f"Hash Gerado: {hash_da_senha}")

# Agora, vamos verificar se a senha original corresponde ao hash
senha_correta = verify_password(senha_original, hash_da_senha)
senha_incorreta = verify_password("senha_errada", hash_da_senha)

print(f"A senha original corresponde ao hash? -> {senha_correta}") # Deve ser True
print(f"Uma senha errada corresponde ao hash? -> {senha_incorreta}") # Deve быть False
print("--- Teste de Segurança Concluído ---\n")


# ====================================================================
# PARTE 2: TESTANDO A CRIAÇÃO DE UM USUÁRIO NO BANCO DE DADOS
# ====================================================================
print("--- Iniciando Teste de Criação de Usuário no DB ---")
from app.database import SessionLocal
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate

# Criamos uma sessão com o banco de dados
db = SessionLocal()

try:
    # 1. Verificamos se o usuário já existe para não dar erro de 'unique'
    print("Verificando se o usuário 'admin_test' já existe...")
    user_in_db = db.query(Usuario).filter(Usuario.username == "admin_test").first()
    
    if user_in_db:
        print("Usuário 'admin_test' já existe no banco. Teste de criação pulado.")
    else:
        # 2. Se não existe, criamos um novo usuário
        print("Criando um novo usuário de teste...")
        novo_usuario_schema = UsuarioCreate(
            username="admin_test",
            password="admin_password", # Senha em texto puro
            role="administrador"
        )

        # 3. Geramos o hash da senha antes de salvar
        hash_senha_novo_usuario = get_password_hash(novo_usuario_schema.password)

        # 4. Criamos a instância do modelo SQLAlchemy com a senha hasheada
        db_novo_usuario = Usuario(
            username=novo_usuario_schema.username,
            hashed_password=hash_senha_novo_usuario,
            role=novo_usuario_schema.role
        )

        # 5. Adicionamos ao banco e salvamos (commit)
        db.add(db_novo_usuario)
        db.commit()
        db.refresh(db_novo_usuario)
        
        print("Usuário 'admin_test' criado com sucesso no banco de dados!")
        print(f"ID: {db_novo_usuario.id}, Username: {db_novo_usuario.username}, Role: {db_novo_usuario.role}")

except Exception as e:
    print(f"Ocorreu um erro ao interagir com o banco de dados: {e}")
finally:
    # 6. É muito importante fechar a sessão com o banco
    db.close()
    print("--- Teste de Criação de Usuário Concluído ---")