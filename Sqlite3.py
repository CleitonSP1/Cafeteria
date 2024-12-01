import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('cafeteria.db')
cursor = conn.cursor()

# Adicionar um usuário administrador
cursor.execute("INSERT INTO user (username, password, is_admin) VALUES ('admin', 'admin', 1)")

# Confirmar a inserção
conn.commit()

# Verificar os dados
cursor.execute("SELECT * FROM user")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Fechar a conexão
conn.close()
