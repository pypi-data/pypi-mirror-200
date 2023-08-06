from setuptools import setup

setup(
    name='ccparo',
    version='0.2',
    packages=['ccparo'],
    install_requires=[
        'requests',
        'pyperclip'
    ],
    entry_points={
        'console_scripts': [
            'cheaters=cheaters.main:main'
        ]
    }
)
