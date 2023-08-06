import setuptools

setuptools.setup(
    name="pummel",
    version="0.14.0",
    description="Minimalist local deployment based on kivalu",
    long_description="TODO",
    long_description_content_type="text/markdown",
    author="Thomas JOUANNOT",
    author_email="mazerty@gmail.com",
    url="https://zebr0.io/projects/pummel",
    download_url="https://gitlab.com/zebr0/pummel",
    packages=["pummel"],
    scripts=["scripts/pummel"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: System"
    ],
    license="MIT",
    install_requires=[
        "kivalu",
        "PyYAML"
    ]
)
