import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.command.install import install


__version__ = "0.0.8"
HERE = Path(__file__).resolve().parent


class CustomInstallCommand(install):
    """Customized setuptools install command - installs the planner first."""
    def run(self):
        install.run(self)
        subprocess.check_call(["./src/state_space_generator/scorpion/build.py"])

def compute_files(subdir):
    return [str(p.resolve()) for p in subdir.rglob('*')]

# Add Fast-Downward files to be copied
files = []
files.append(str(Path("src/state_space_generator/scorpion/fast-downward.py").resolve()))
files.append(str(Path("src/state_space_generator/scorpion/build.py").resolve()))
files.append(str(Path("src/state_space_generator/scorpion/build_configs.py").resolve()))
files.append(str(Path("src/state_space_generator/scorpion/LICENSE.md").resolve()))
files.append(str(Path("src/state_space_generator/scorpion/README.md").resolve()))
files.extend(compute_files(Path("src/state_space_generator/scorpion/driver")))
files.extend(compute_files(Path("src/state_space_generator/scorpion/src")))
files.extend(compute_files(Path("src/state_space_generator/scorpion/builds/release/bin")))

setup(
    name="state_space_generator",
    version=__version__,
    license='GNU',
    author="Dominik Drexler, Jendrik Seipp",
    author_email="dominik.drexler@liu.se, jendrik.seipp@liu.se",
    url="https://github.com/drexlerd/state-space-generator",
    description="A tool for state space exploration of PDDL files",
    long_description="",
    packages=['state_space_generator'],
    package_dir={'state_space_generator': 'src/state_space_generator'},
    package_data={'': files},
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'install': CustomInstallCommand,
    },
)
