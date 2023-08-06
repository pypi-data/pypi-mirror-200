# Prepare
```shell
cd path/to/lib_repo_tool
pip install -r requirements.txt
```
Suggest to use the Python virtual environment to install the Python libraries.
Reference: [How to setup virtual environment](https://www.liaoxuefeng.com/wiki/1016959663602400/1019273143120480)

# Download libs from repository
1. create the dependencies.json file in you project. The file contains the libs' name and version that your project depends on.
```json
{
  "lib name": "lib version or null"
}
```
2. Execute the command
```shell
python path/to/lib_get.py --dep path/to/dependencies.json --dest path/to/libs/dir
```

# Add lib to repository
Execute the command
```shell
python path/to/lib_repo.py --path path/to/lib --platform windows --version 1.0  
```