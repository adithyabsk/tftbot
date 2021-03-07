from setuptools import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="roambot",
    version="0.1",
    description="A Roam Twitter Bot",
    url="",
    author="Adithya Balaji",
    author_email="",
    license="MIT",
    packages=["roambot"],
    install_requires=required,
    zip_safe=False,
)
