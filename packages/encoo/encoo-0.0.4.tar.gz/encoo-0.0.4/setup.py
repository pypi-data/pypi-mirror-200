from setuptools import find_packages, setup

setup(
    name='encoo',
    version='0.0.4',
    packages=find_packages(),
    install_requires=['xlwt>=1.3.0', 'xlrd>=2.0.1', 'configparser>=5.3.0']
)


# 打包 python .\setup.py sdist bdist_wheel
# 上传 twine upload dist/*
# username:__token__
# password:pypi-AgEIcHlwaS5vcmcCJDc1NDExMmY1LTgyNGItNDczZC1iN2I5LWYwNmVmYjVjMmE5NgACDVsxLFsiZW5jb28iXV0AAixbMixbIjZhYjY4NWU5LTBmYzUtNDM3MS05YTMxLTFiNzdhY2U5Zjc2YiJdXQAABiCv2ko-wuD4xlL3eG3U0mr7-74pK-rkJYheJ4GtdedoTQ

# 安装 pip install encoo==0.0.1  -i https://www.pypi.org/simple/
