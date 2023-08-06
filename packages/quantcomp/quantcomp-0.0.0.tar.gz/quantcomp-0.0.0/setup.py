import setuptools

INSTALL_REQUIREMENTS = ['numpy', 'torch', 'torchvision', 'tqdm']

setuptools.setup(
    description='quantcomp',
    author='Felix Petersen',
    author_email='ads0361@felix-petersen.de',
    version='0.0.0',
    name='quantcomp',
    packages=[],
    install_requires=INSTALL_REQUIREMENTS,
)
