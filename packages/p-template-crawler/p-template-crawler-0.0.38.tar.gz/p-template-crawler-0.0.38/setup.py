import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="p-template-crawler",
    version="0.0.38",
    author="pengjun",
    author_email="mr_lonely@foxmail.com",
    description="template tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=[],
    install_requires=[
        'requests',
        'oss2',
        'Image',
        'Pillow',
        'fake_useragent'
    ],
    dependency_links=[],
    entry_points={
        'console_scripts':[
            'crawler = mecord_crawler.main:main'
        ]
    },
    python_requires='>=3.7',
)