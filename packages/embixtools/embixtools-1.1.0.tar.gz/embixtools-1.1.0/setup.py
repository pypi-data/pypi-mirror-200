from setuptools import setup

setup(
    name = 'embixtools',
    version = '1.1.0',
    description = 'EMBIX tools',
    packages = ['embixtools'],
    install_requires = [
        'pytz', 
        'requests', 
        'oauthlib', 
        'requests_oauthlib',
        'pyyaml'
    ],
)