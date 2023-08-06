from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='nonebot_paddle_ocr',  # 包名
      version='1.0.0',  # 版本号
      description='A ocr bot on qq',
      long_description=long_description,
      author='canxin',
      author_email='1969730106@qq.com',
      url='https://github.com/canxin121/nonebot_paddle_ocr',
      install_requires=[],
      license='Apache License 2.0',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],
      )
