from setuptools import setup, find_packages

setup(
    name='gpt_code_review',
    version='0.1.0',
    packages=find_packages(),
    author='Patryk Maruda',
    author_email='patrykmaruda@gmail.com',
    description='Code review with GPT-3',
    install_requires=[
        'click',
        'openai',
    ],
    entry_points='''
        [console_scripts]
        gpt_code_review=gpt_code_review.main:SomeFunctionClass.cli
    '''
)