from setuptools import setup, find_packages


with open('README.md') as readme:
    long_description = readme.read()


with open('requirements.txt') as requirements:
    dependencies = [line.strip() for line in requirements]


setup(
    name='endermite',
    version='0.0.5',
    license='MIT',
    description='A high-level, opinionated python framework for building Minecraft data packs',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Valentin Berlier',
    author_email='berlier.v@mail.com',
    url='https://github.com/vberlier/endermite',

    platforms=['any'],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='minecraft datapack python framework mcfunction map-making',

    packages=find_packages(),

    install_requires=dependencies,

    entry_points={
        'console_scripts': [
            'ender=endermite.cli:ender',
        ],
    },
)
