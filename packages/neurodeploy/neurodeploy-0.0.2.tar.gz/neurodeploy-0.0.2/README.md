
#Generate doc
sphinx-apidoc -o doc/source/ ./neurodeploy
sphinx-build -b html doc/source doc/build
sphinx-build -b pdf doc/source doc/build
#find pdf under doc/build

##################################"

venv 
python -m venv  venv
source venv/bin/activate

subcmd -> querie -> utils -> query // get data
                 -> proceess -> utils ->  file //process data
#######################################################################
//help
 python cli.py  --help
 python cli.py  model --help

1-Auth to API

 - By getting yout token
   //user login
   python cli.py  user login  --username YOUR_USER_NAME  --password YOUR_PASSWORD

2- create and upload your model
 
 //model push
 python cli.py model push --name YOUR_MODEL_NAME --file-path /YOUR_PATH/YOUR_MODEL_FILE_NAME

3- predict your model
 python cli.py model predict --name YOUR_MODEL_NAME  --data '{"payload": [[1, 2, 3, 4, 5]]}'


Other useful cmd: 

//model delete
 python cli.py  model delete  --name YOUR_MODEL_NAME
//model list
 python cli.py  model list
//model_get
 python cli.py  model get  --name YOUR_MODEL_NAME


//create credential
 python cli.py  credentials create --name CREDENTIAL_NAME  --description YOUR_DESC
//delete credential
 python cli.py  credentials delete  --name CREDENTIAL_NAME
//list credentials
 python cli.py  credentials list


###############################################
run test sh test.py 
###############################################
build package

python -m pip install –-user –-upgrade setuptools wheel
python setup.py sdist bdist_wheel

twine check dist/*
twine upload dist/*
python -m twine upload dist/*
###############################################
Build binary 
sh bin.sh
you can find bin file here
dist/cli



