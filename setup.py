import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lazyuptimerobot.py",
    version="1.0.1",
    author="Michal Frontczak",
    author_email="michaljev@o2.pl",
    description="API Client for uptimerobot.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fxa90id/lazyuptimerobot.py",
    packages=setuptools.find_packages(),
    keywords="lazy uptimerobot",
    install_requires=["requests", "urllib3"],
    python_requires='>=2.7',
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
