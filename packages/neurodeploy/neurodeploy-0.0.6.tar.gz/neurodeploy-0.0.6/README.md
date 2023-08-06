


# Quick start With SDK

> Welcome to neurodeploy SDK

> The SDK is under directory neurodeploy

  1. Install python package:

   `pip install neurodeploy`

  2. Import the library:

   `import neurodeploy as nd`

  2. Auth to API:

   - By getting your JWT token

   `nd.user.login(your_username,your_password)`

  3. Create and upload your model:

   - Model push

   `nd.model.push(your_model_name,your_model_file_path,libray_forml,file_extention)`

  4. Predict your model:

   `nd.model.predict(your_model_name,your_data)`


# Quick start With CLI

> Welcome to neurodeploy CLI

  1. Pull the repo:

   `git pull REPO_URL`

  2. Auth to API:
   - By getting your JWT token
  
   `python neuro.py  user login  --username YOUR_USER_NAME  --password YOUR_PASSWORD`
  
  3. Create and upload your model:
   - Model push
  
   `python neuro.py model push --name YOUR_MODEL_NAME --file-path /YOUR_PATH/YOUR_MODEL_FILE_NAME`
  
  4. Predict your model:
  
   `python neuro.py model predict --name YOUR_MODEL_NAME  --data '{"payload": [[1, 2, 3, 4, 5]]}'`
  
---
# CLI usage
---
  ### CLI help
 `python cli.py  --help`

 `python cli.py  model --help`

  ### CLI usage
   #### Authentificate CLI:

  There si differents way to connect your cli to neurodeploy:

    1.By JWT token                 : For simple temporary usage

    2.By access_key and secret_key : For ci/cd pipeline

    3.By cli config                : For user admin computer

  1. By JWT token:

  - Excute cli cmd login to get your jwt token  with you username password for your account created by the UI

    `python cli.py  user login  --username YOUR_USER_NAME  --password YOUR_PASSWORD` 

         `jwt token is stored locally and expire each 24 hours need to login a second time to renew your token
`
  2. By access_key and secret_key

  - Get you acces key secret key from the ui

  - Set envirement variables:

    `export ND_SECRET_KEY="xxxxxxxxxxx"`   

    `export ND_ACCESS_KEY="xxxxxxxxxxx"`

         `credentials ares stored locally in your machine no expiration`

  3. By cli config

  - Execute cli conf file with you username password for your account created by the UI

    `python cli.py  configure update`

         `Save cli config`

         `Enter your username: your_user_name`

         `Enter your password: xxxx`

         `Repeat for confirmation: xxx`


   #### Using CLI:
   ##### Managing model 

- Delete model: 

 `python cli.py  model delete  --name YOUR_MODEL_NAME`
- List models:

 `python cli.py  model list`
- Get model:

 `python cli.py  model get  --name YOUR_MODEL_NAME`

   ##### Managing credentials
- Create credential

 `python cli.py  credentials create --name CREDENTIAL_NAME  --description YOUR_DESC`
- Delete credential

 `python cli.py  credentials delete  --name CREDENTIAL_NAME`
- List credentials

 `python cli.py  credentials list`

---
# Generate doc
  - Execute bash script to build doc: doc.sh

   `sh doc.sh`

     You can find pdf under doc/build

---
# Venv and requirement
  - To activate venv

   `source venv/bin/activate`

  - Install requirement: 

   `pip install -r  requirements.txt`
---
# Run tests
  - Execute bash script for tests

  `sh test.sh`

---
# Build package
  - Execute bash script for build

  `sh build.sh`
---
# Build CLI Binary
  - Execute bash script for build binary

  `sh bin.sh `

    You can find bin file here dist/cli
---
# Env vars
| ENV VAR Name | Description | Values | 
|--------------|:-----------:|:------:|
|  ND_SECRET_KEY         |    User acces key value to auth to api |xxxx
|  ND_ACCESS_KEY         |    User secret key value to auth to api|xxxx
|  ND_DEFAULT_LIB        |    Default ml library used|tensorflow/sklearn
|  ND_DEFAULT_FILETYPE   |    Default ml model file extention|H5/pickel
|  ND_DEFAULT_CONFDIR    |    Default cli configuration path to store username / token / credentials|~.nd
|  ND_DEFAULT_ENDPOINT   |    Default neurodeploy endpoint domain name|.neurodeploy.com


---


