Sistema de Autenticação em Python

Este projeto apresenta um sistema de autenticação simples desenvolvido em Python, utilizandoo MySQL
para armazenamento de dados dos usuários.Este código serve como uma base sólida e pode ser facilmente 
integrado a um sistema mais amplo, como um sistema de telas (GUI) ou conectado a um servidor SQL.

Recursos
Cadastro de Usuários: Permite aos usuários criar contas no sistema, armazenando informações como nome, 
e-mail, idade e senha de forma segura.

Login de Usuários: Facilita o login dos usuários verificando as credenciais no banco de dados MySQL. 
A senha é armazenada de maneira segura usando o algoritmo de hash MD5.

Verificação de Conta: Fornece um mecanismo de verificação de conta por e-mail utilizando autenticação 
de dois fatores (2FA) com o auxílio da biblioteca PyOTP. Os códigos são enviados por e-mail e expiram 
após um intervalo de tempo.

Integração com MySQL: Utiliza a biblioteca mysql-connector para se comunicar com um banco de dados MySQL. 
As funções alter_mysql, read_mysql, login_mysql e change_2fa_in_mysql mostram como interagir com 
o banco de dados.

Como Usar

Configuração do Ambiente:

Instale as dependências necessárias utilizando o comando: pip install -r requirements.txt.
Configure as variáveis de ambiente no arquivo .env para conexão com o banco de dados e chaves de API.

Execução do Código:

Execute o script principal main.py para iniciar a interação com o sistema.
Integração com Outros Componentes:

Este código serve como uma base que pode ser facilmente integrada a sistemas de interface gráfica (GUI) 
ou a servidores SQL mais complexos. Este projeto é uma base sólida para desenvolver sistemas de autenticação 
mais robustos e pode ser adaptado conforme as necessidades específicas do seu projeto. Lembre-se de consultar 
a documentação para obter informações detalhadas sobre cada componente.
