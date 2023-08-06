from setuptools import setup, find_packages

setup(
    name='sinai-corpus',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List any dependencies here
    ],
    entry_points={
        'console_scripts': [
            'sinai-corpus-generate=sinai_corpus.generate:main',
            'sinai-corpus-load=sinai_corpus.load:main',
        ],
    },
    # metadata to display on PyPI
    author='Mohab Mes',
    author_email='mohabmes@email.com',
    description='A corpus of text documents from the Sinai peninsula',
    license='MIT',
    keywords='corpus nlp',
    url='https://github.com/mohabmes/Sinai-corpus',
    package_data={
        'sinai_corpus': ['src/Sinai-corpus.zip'],
    },
)
