from setuptools import setup, find_packages

setup(
    name='tg-hours',
    version='1.2.0',
    packages=find_packages(),
    url='https://github.com/taylorhickem/nt-hours',
    description='add-on utility for time tracking report using Toggl Track time tracker app',
    author='@taylorhickem',
    long_description=open('README.md').read(),
    install_requires=open("requirements.txt", "r").read().splitlines(),
    include_package_data=True,
    entry_points={
            'console_scripts': [
                'tghours = tghours.__main__:run',
            ]
    }
)