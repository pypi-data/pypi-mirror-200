from struct import pack
from  setuptools import setup, find_packages

setup(
    name='Mensajes-agiraldomolina',
    version='6.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type ='text/markdown',
    author='Alba Giraldo',
    author_email='agiraldomolina@gmail.com',
    url='',
    packages=find_packages(),
    scripts=[],
    test_suite = 'test',
    install_requires = [paquete.strip() for paquete in open('requirements.txt').readlines()],
    classifiers=['Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.0',
                 'Topic :: Utilities',
                 ],
    
)

