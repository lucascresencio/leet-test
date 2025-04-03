Tutorial Guillian:

Instale os seguintes programas: 
Postman
Pycharm community - https://www.jetbrains.com/pycharm/download/
Git - https://git-scm.com/downloads
Python 3.12

Entre em uma pasta onde deseja clonar esse repositório e clique com o botão direito e depois na opção "git bash"
no console do git escreva: git clone https://github.com/lucascresencio/leet.git

Depois abra o pycharm e selecione a basta do projeto que foi criada com o git
Clique no icone do git no canto inferior esquerdo dentro do pycharm e clique em fetch all remotes
Abra terminal no pycharm digite e instale as seguintes dependencias:
pip install fastapi
pip install uvicorn
pip install supabase python-dotenv

Depois disso é só rodar:
para rodar voce abre o terminal de novo e escreve: uvicorn main:app --reload
ele vai logar uma mensagem mais ou menos assim:
INFO:     Will watch for changes in these directories: ['/Users/macbookpro/PycharmProjects/PythonProject']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [3148] using StatReload

o endereço http que aparecer é o seu servidor local, e por lá vc consegue fazer as chamadas no postman
vou colocar um curl de exemplo da chamada de post para criar um mantenedor:
curl --location 'http://127.0.0.1:8000/maintainers' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "hank@leet.com",
    "name": "Hank Rearden",
    "phone": 16936181765,
    "cpf": 45688167858,
    "birthday": "1970-08-12",
    "zip": "13563673",
    "street": "Otto Werner Rosel",
    "neighborhood": "Jardim Ipanema",
    "number": "1455",
    "complement": "moradas",
    "city": "São Carlos",
    "state": "SP",
    "member_since": "1970-08-12",
    "org_id": 0,
    "role_id": 4,
    "status": "activated"
}'
