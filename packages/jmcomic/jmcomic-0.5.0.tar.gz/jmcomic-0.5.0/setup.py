from setuptools import setup, find_packages

with open("README.md", 'r', encoding='utf-8') as f:
    long_description = f.read()

version = '0.5.0'

setup(
    name='jmcomic',
    version=version,

    description='Python API For JMComic (禁漫天堂)',
    long_description_content_type="text/markdown",
    long_description=long_description,

    url='https://github.com/hect0x7/JMComic-Crawler-Python',
    author='hect0x7',
    author_email='93357912+hect0x7@users.noreply.github.com',

    packages=find_packages(),
    install_requires=[
        'commonX',
        'curl_cffi',
        'PyYAML',
        'Pillow',
        'setuptools',
    ],
    python_requires=">=3.7",

    keywords=['python', 'jmcomic', '18comic', '禁漫天堂', 'NSFW'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
