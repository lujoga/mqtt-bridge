from setuptools import setup

setup(
    name='mqtt-bridge',
    packages=['bridge'],
    include_package_data=True,
    install_requires=[
        'paho-mqtt',
    ],
    entry_points={
        'console_scripts': [
            'mqtt-bridge=bridge.__main__:main'
        ]
    }
)
