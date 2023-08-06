from setuptools import setup, find_packages

setup(
    name='ColorsAndStyles',
    version='0.0.3',
    description='A basic package that makes it easy to add color and styles to your terminal.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    author='QwertyQwerty',
    author_email='personqwertyperson88@gmail.com',
    license='MIT', 
    keywords=['color', 'style', 'ansi'], 
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=find_packages(),
    install_requires=[''] 
)