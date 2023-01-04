from setuptools import setup, find_packages

setup(
    name="kyotoshogi-ai",
    version='1.0.0',
    package=find_packages(),
    include_package_data=True,
    install_requires=[
        "tensorflow",
        "pillow",
    ],
     entry_points={
            'console_scripts':[
                'play=kyotoshogi_ai.human_play:main',
                'train=kyotoshogi_ai.train_cycle:main',
            ],
        },
)