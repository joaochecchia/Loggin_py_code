import mysql.connector
from hashlib import md5
from dotenv import load_dotenv
from b import enviar_email
import time
import pyotp
import os

load_dotenv()

class User:
    
    def __init__(self, user_name, user_email, user_age, password):
        # Initialize User object with basic information
        self.user_name = user_name
        self.user_email = user_email
        self.user_age = user_age
        self.password = password
        self.user_2fa = False  # Initially, 2FA is set to False
    
    def alter_mysql(self, cursor, conexao):
        # Add user information to the MySQL database
        hashed_password = self.hash_password(self.password)
        cursor.execute("""INSERT INTO user_info (user_name, user_email, user_age, password_)
                        VALUES(%s, %s, %s, %s);""",
                       (self.user_name, self.user_email, self.user_age, hashed_password))
        conexao.commit()
    
    def read_mysql(self, cursor):
        # Read all user information from the MySQL database
        cursor.execute('SELECT * FROM user_info;')
        return cursor.fetchall()
    
    def login_mysql(self, cursor):
        # Log in the user by checking credentials in the MySQL database
        if self.user_name is not None:
            print('Você já está logado')
        else:
            user_info = self.read_mysql(cursor)
            check_user = input('Digite seu email: ')

            for user in user_info:
                if check_user == user[2]:
                    print('Usuário encontrado')
                    break
            else:
                print('Usuário não encontrado')
                return

            check_password = input('Digite sua senha: ').encode('utf8')
            hashed_password = md5(check_password).hexdigest()

            for user in user_info:
                if hashed_password == user[4] and check_user == user[2]:
                    print('Você está logado')
                    self.set_user_info(user)
                    break
            else:
                print('Senha errada')
    
    def set_user_info(self, user):
        # Set user information based on database entry
        self.user_name = user[1]
        self.user_email = user[2]
        self.user_age = user[3]
        self.user_password = user[4]
        self.user_2fa = user[5]
    
    def verify_account(self):
        # Send a verification code to the user's email and verify it
        totp = pyotp.TOTP(os.getenv('API_KEY'), interval=60)
        code = totp.now()
        enviar_email(self.user_email, code)
        print('O código expira em 90 segundos')

        timer = time.time()
        verified = False

        while time.time() < timer + 90:
            verify_code = input('Digite o código: ')
            try_ = totp.verify(int(verify_code))

            if try_:
                verified = True
                print('Você verificou seu email')
                break

        if not verified:
            print('Tempo expirado')
        
    def change_2fa_in_mysql(self, cursor, conexao):
        # Enable 2FA for the user in the MySQL database
        self.verify_account()

        cursor.execute("""UPDATE user_info
                           SET two_fa = TRUE
                           WHERE user_name = %s""", (self.user_name,))
        conexao.commit()

    @staticmethod
    def hash_password(password):
        # Hash the password using md5
        return md5(password.encode('utf8')).hexdigest()

# Establish a connection to the MySQL database
conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE"),
)

cursor = conexao.cursor()

while True:
    # Main user interaction loop
    choice = input("Digite [L]ogin, [S]ign-in, Log [O]ff, [V]erify account ou [E]xit: ")

    if choice.lower() == 's':
        # User chooses to sign up
        user_name = input('Digite seu nome: ').lower()
        user_email = input('Digite seu email: ')
        user_age = int(input('Digite sua idade: '))
        password = input('Digite sua senha (senha > 4 caracteres): ')

        while len(password) <= 4:
            password = input('Erro!!! Digite uma senha com mais de 4 caracteres: ')

        password_2 = input('Verifique sua senha: ')

        while password != password_2:
            password_2 = input('Erro!!! As senhas não coincidem. Digite novamente: ')

        user = User(user_name, user_email, user_age, password)
        user.alter_mysql(cursor, conexao)
        
    elif choice.lower() == 'l':
        # User chooses to log in
        try:
            user = User(None, None, None, None)
            user.login_mysql(cursor)
        except Exception as e:
            print(f'Erro: {e}')
    
    elif choice.lower() == 'o':
        # User chooses to log off
        user = User(None, None, None, None)
        print('Você saiu da conta')

    elif choice.lower() == 'v':
        # User chooses to verify account (enable 2FA)
        if user.user_2fa:
            print('Você já é autenticado')
        elif not user.user_2fa:
            user.change_2fa_in_mysql(cursor, conexao)

    elif choice.lower() == 'e':
        # User chooses to exit the program
        break

# Close cursor and database connection
cursor.close()
conexao.close()
