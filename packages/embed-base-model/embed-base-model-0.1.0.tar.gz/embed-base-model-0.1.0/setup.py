import setuptools

setuptools.setup(
    name='embed-base-model',
    version='0.1.0',
    license='Apache-2.0',
    author='Daniel Lee',
    author_email='rootuser.kr@gmail.com',
    description='Python abstract class for embedding sentences',
    long_description=open('README.md').read(),
    url='https://github.com/asulikeit/embed-base-model',
    packages=['embedmodel'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ]
)