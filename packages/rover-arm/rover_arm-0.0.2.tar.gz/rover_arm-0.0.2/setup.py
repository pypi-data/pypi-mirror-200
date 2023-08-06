import setuptools
from pathlib import Path

setuptools.setup(
    name='rover_arm',
    version='0.0.2',
    description="A OpenAI Gym Env for Rover with Arm",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages = setuptools.find_packages(include="rover_arm*"),


    install_requires=['gym', 'pybullet']  # And any other dependencies foo needs
)
