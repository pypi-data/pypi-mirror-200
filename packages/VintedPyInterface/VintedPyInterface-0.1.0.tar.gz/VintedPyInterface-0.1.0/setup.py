from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name='VintedPyInterface',
    version='0.1.0',
    description='Interface for Vinted front end',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ProfesseurIssou/VintedPyInterface',
    author='Alix Hamidou',
    author_email='alix.hamidou@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'selenium==4.6.1',
        'fake_useragent==1.1.3',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
