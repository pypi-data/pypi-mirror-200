from setuptools import find_packages, setup

VERSION = '1.0'

with open('README.md', 'r', encoding='gbk') as fp:
    long_description = fp.read()

setup(
    name='ocrdll', # 模块名称
    version=VERSION, # 当前版本
    author='lixin', # 作者
    author_email='', # 作者邮箱
    description='ocrdll', # 模块简介
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    keywords='',
    packages=find_packages(),
    include_package_data=True,

    #install_requires=['urllib3 >= 1.0'],
    python_requires='>=3.0',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
)
