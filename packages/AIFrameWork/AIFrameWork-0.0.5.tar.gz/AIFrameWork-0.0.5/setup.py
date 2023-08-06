from setuptools import setup, find_packages

setup(
    name='AIFrameWork',
    version='0.0.5',
    packages=find_packages(),
    author='Maurya Vijayaramachandran',
    author_email='maurya.mvr@gmail.com',
    description='A library for performaing machine learning tasks with ease',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'matplotlib'
    ],
)
