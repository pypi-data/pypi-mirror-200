from setuptools import setup, find_packages

setup(
    name='lib_repo_tool',
    version='2.0.2',
    author='Andy Zhuang',
    author_email='xiaolong.zhuang@gmail.com',
    description='Put depended libs to oss file bucket',
    install_requires=['oss2==2.14.0', 'dacite==1.6.0', 'tabulate'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lib-get=repo_tool:lib_get',
            'lib-repo=repo_tool:lib_repo'
        ]
    }
)