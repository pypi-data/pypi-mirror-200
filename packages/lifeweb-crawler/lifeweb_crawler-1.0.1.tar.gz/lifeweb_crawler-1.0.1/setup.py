import setuptools

setuptools.setup(
    name='lifeweb_crawler',
    version='1.0.1',
    author='anonymous',
    author_email='lifeweb.crawler@gmail.com',
    description='This package allows the use of lifeweb EDGE server',
    url='',
    # project_urls={
    #     "Bug Tracker": ""
    # },
    packages=['lifeweb_crawler'],
    python_requires=">=3",
    install_requires=[
        "requests",
        "fastapi",
        "pika",
        "python-logstash",
        "python-jose",
        "passlib",
    ],
)
