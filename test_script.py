

# ====================================================================
# PARTE 1: TESTANDO AS FUNÇÕES DE SEGURANÇA (SENHAS)
# ====================================================================
print("--- Iniciando Teste de Segurança ---")
from app.security import get_password_hash, verify_password

senha_original = "senha_super_secreta"
hash_da_senha = get_password_hash(senha_original)

print(f"Senha Original: {senha_original}")
print(f"Hash Gerado: {hash_da_senha}")

senha_correta = verify_password(senha_original, hash_da_senha)
senha_incorreta = verify_password("senha_errada", hash_da_senha)

print(f"A senha original corresponde ao hash? -> {senha_correta}")
print(f"Uma senha errada corresponde ao hash? -> {senha_incorreta}")
print("--- Teste de Segurança Concluído ---\n")


# ====================================================================
# PARTE 2: TESTANDO A CRIAÇÃO DE USUÁRIOS NO BANCO DE DADOS
# ====================================================================
print("--- Iniciando Teste de Criação de Usuário no DB ---")
from app.database import SessionLocal
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate

db = SessionLocal()

try:
    # --- BLOCO 1: Garante que o usuário ADMINISTRADOR existe ---
    print("Verificando se o usuário 'admin_test' já existe...")
    user_in_db = db.query(Usuario).filter(Usuario.username == "admin_test").first()
    
    if user_in_db:
        print("Usuário 'admin_test' já existe no banco. Criação pulada.")
    else:
        print("Criando o usuário 'admin_test'...")
        novo_usuario_schema = UsuarioCreate(
            username="admin_test",
            password="admin_password",
            role="administrador"
        )
        hash_senha_novo_usuario = get_password_hash(novo_usuario_schema.password)
        db_novo_usuario = Usuario(
            username=novo_usuario_schema.username,
            hashed_password=hash_senha_novo_usuario,
            role=novo_usuario_schema.role
        )
        db.add(db_novo_usuario)
        db.commit()
        db.refresh(db_novo_usuario)
        print("Usuário 'admin_test' criado com sucesso!")

    # --- BLOCO 2: Garante que o USUÁRIO COMUM existe (AJUSTADO) ---
    print("\nVerificando se o usuário 'user_test' já existe...") # <-- AJUSTADO
    user_comum_in_db = db.query(Usuario).filter(Usuario.username == "user_test").first() # <-- AJUSTADO

    if user_comum_in_db:
        print("Usuário 'user_test' já existe no banco. Criação pulada.") # <-- AJUSTADO
    else:
        print("Criando o usuário 'user_test'...") # <-- AJUSTADO
        novo_usuario_comum_schema = UsuarioCreate(
            username="user_test",         # <-- AJUSTADO
            password="user_password",     # <-- AJUSTADO
            role="usuario"
        )
        hash_senha_novo_comum = get_password_hash(novo_usuario_comum_schema.password)
        db_novo_usuario_comum = Usuario(
            username=novo_usuario_comum_schema.username,
            hashed_password=hash_senha_novo_comum,
            role=novo_usuario_comum_schema.role
        )
        db.add(db_novo_usuario_comum)
        db.commit()
        db.refresh(db_novo_usuario_comum)
        print("Usuário 'user_test' criado com sucesso!") # <-- AJUSTADO


except Exception as e:
    print(f"Ocorreu um erro ao interagir com o banco de dados: {e}")
finally:
    db.close()
    print("\n--- Teste de Criação de Usuário Concluído ---")