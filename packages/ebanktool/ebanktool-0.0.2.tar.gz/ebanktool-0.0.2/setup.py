from setuptools import find_packages, setup

setup(
    name='ebanktool',
    version='0.0.2',
    packages=find_packages(),
    install_requires=['xlwt>=1.3.0', 'xlrd>=2.0.1',
                      'pdfplumber>=0.8.0', "encoo>=0.0.3",
                      "python-dateutil>=2.8.2", "pypdf>=3.6.0", "requests>=2.28.2", "urllib3>=1.26.14"]
)


# 打包 python .\setup.py sdist bdist_wheel
# 上传 twine upload dist/*
# 安装 pip install ebanktool==0.0.1  -i https://www.pypi.org/simple/
