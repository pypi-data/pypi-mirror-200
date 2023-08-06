from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience  :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='fisikaSMA',
    version='0.0.3',
    description='Phisics Function',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read() + '\n\n' + open('USE.txt').read(),
    url='',
    author='KS2_Kelompok 1',
    author_email='',
    license='MIT',
    classifiers=[],
    keywords='fisika',
    packages=find_packages(),
    install_required=['']
)