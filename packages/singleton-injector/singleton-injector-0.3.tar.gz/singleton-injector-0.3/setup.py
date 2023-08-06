from distutils.core import setup

setup(
    name="singleton-injector",
    packages=["singleton_injector"],
    version="0.3",
    license="MIT",
    description="Simple library to unify singleton and injection with a decorator",
    author="Santiago Melo Medina",
    author_email="smelomedina05@gmail.com",
    url="https://github.com/santiagoMeloMedina/singleton-injector",
    download_url="https://github.com/santiagoMeloMedina/singleton-injector/archive/refs/tags/0.2.tar.gz",
    keywords=[
        "Injection",
        "Singleton",
        "Simple",
    ],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
    ],
)
