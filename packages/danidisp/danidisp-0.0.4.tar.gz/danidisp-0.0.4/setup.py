from setuptools import setup

setup(
    name="danidisp",
    version='0.0.4',
    description='My package, every useful function I want to use',
    py_modules=['danidisp'],
    package_dir={'': 'src'},
    url="https://github.com/DanieleDiSpirito/danidisp",
    author="Daniele Di Spirito",
    author_email="danieledisp@proton.me",
    long_description='''
        Package contains:\n
        - xor(a: bytes, b: bytes) -> bytes
        - dlog(n: int, b: int, mod: int) -> int
    '''
)