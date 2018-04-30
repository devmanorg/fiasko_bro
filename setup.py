from setuptools import setup, find_packages
from setuptools.command.install import install
from os import path


here = path.abspath(path.dirname(__file__))


def load_requirements():
    requirements = list(line.split()[0] for line in open("requirements.txt"))
    return requirements


class InstallWithCompile(install):
    def run(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog(self.distribution)
        option_dict = self.distribution.get_option_dict('compile_catalog')
        compiler.domain = [option_dict['domain'][1]]
        compiler.directory = option_dict['directory'][1]
        compiler.run()
        super().run()


setup(
    packages=find_packages(),
    # since babel appears both in setup_requires and install_requires,
    # our package can't be instaled with python setup.py install command
    # see https://github.com/pypa/setuptools/issues/391
    setup_requires=['babel'],
    install_requires=load_requirements(),
    entry_points={
        'console_scripts': [
            'fiasko = bin.fiasko:main',
        ],
    },
    cmdclass={
        'install': InstallWithCompile,
    },
    package_data={'': ['locale/*/*/*.mo', 'locale/*/*/*.po']},
)
