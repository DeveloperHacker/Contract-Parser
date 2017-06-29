from distutils.core import setup

setup(
    name='contracts',
    version='1.0',
    packages=[
        'contracts',
        'contracts.nodes',
        'contracts.tokens',
        'contracts.parser',
        'contracts.visitors',
        'contracts.guides'
    ],
    url='https://github.com/DeveloperHacker/contracts',
    license='MIT',
    author='HackerMadCat',
    author_email='hacker.mad.catgmail.com',
    description='Tiny contract contracts',
    install_requires=[
        'pyparsing'
    ],
)
