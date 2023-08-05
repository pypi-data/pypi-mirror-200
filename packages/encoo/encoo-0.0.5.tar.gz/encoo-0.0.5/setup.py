from setuptools import find_packages, setup

setup(
    name='encoo',
    version='0.0.5',
    packages=find_packages(),
    install_requires=['xlwt>=1.3.0', 'xlrd>=2.0.1', 'configparser>=5.3.0']
)


# 打包 python .\setup.py sdist bdist_wheel
# 上传 twine upload dist/*

# 安装 pip install encoo==0.0.1  -i https://www.pypi.org/simple/
