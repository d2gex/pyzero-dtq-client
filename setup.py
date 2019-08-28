import setuptools
import pyzero_dtq_client


def get_long_desc():
    with open("README.rst", "r") as fh:
        return fh.read()


setuptools.setup(
    name="pyzero-dtq-client",
    version=pyzero_dtq_client.__version__,
    author="Dan G",
    author_email="daniel.garcia@d2garcia.com",
    description="A small Producer/Subscriber client to work with a pyzero-dtq server",
    long_description=get_long_desc(),
    long_description_content_type="text/x-rst",
    url="https://github.com/d2gex/pyzero-dtq-client",
    packages=['pyzero_dtq_client'],
    python_requires='>=3.6',
    install_requires=['producer-sink-zmq>=0.1.3', 'pubsub-zmq>=0.1.1'],
    dependency_links=[
        "git+https://github.com/d2gex/producer-sink-zmq.git@0.1.3#egg=producer-sink-zmq",
        "git+https://github.com/d2gex/pubsub-zmq.git@0.1.1#egg=pubsub-zmq"
    ],
    tests_require=['pytest>=5.0.1'],
    platforms='any',
    zip_safe=True,
    classifiers=[
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
