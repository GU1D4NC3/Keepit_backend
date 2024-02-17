# Momsaeng Backend

Fastapi project

Tested with Python 3.11.4


### REQUIREMENT
```
pip install -r requirements.txt
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
```

### update pip
```
python -m pip install --upgrade pip
```

### setup google api key
```os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'googlekey.json'```

### googlekey.json example
```json
{
  "type": "service_account",
  "project_id": "solchell",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "",
  "universe_domain": "googleapis.com"
}
```

### database requirement
please import /sql/MomGroundDatabase.sql to your database

### config.ini
```ini
[account]
db_host=
db_port=
db_user=
db_password=
db_scheme=
[google]
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=
[auth]
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```


### Start application with itself
```shell
python3 main.py
```

### Start with uvicorn
```shell
 uvicorn main:app --port <port>
```