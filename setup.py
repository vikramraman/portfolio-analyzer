from setuptools import setup, find_packages

setup(
    name='analyzer',
    version='0.1',
    author='Vikram Raman',
    author_email='vikram.raman@gmail.com',
    url='https://github.com/vikramraman/portfolio-analyzer',
    license='MIT',
    description='Command line portfolio analyzer',
    long_description='Command line portfolio analyzer',
    py_modules=['analyzer'],
    install_requires=['requests', 'tabulate'],
    entry_points={
        'console_scripts': [
            'analyzer=analyzer:main'
        ]
    }
)
