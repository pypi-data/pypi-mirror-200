# import setuptools
# setuptools.setup(
#     name="omarlibone",
#     version="1.1",
#     author="omar Style",
#     description="omar aAAA",
#     packages=setuptools.find_packages(),
#     classifiers=[
#     "Programming Language :: Python :: 3 ",
#     "Operating System :: OS Independent",
#     "Natural Language :: English",
#     "License :: OSI Approved :: MIT License"
#     ]
    
# )

import setuptools
with open('README.md', 'r') as fh:
    long_description = fh.read()
# with open('requirements.txt','r') as fr:
#     requires = fr.read().split('\n')

setuptools.setup(
    name='omarppplp',
    version="0.2",
    author='omar Style',
    author_email='omarllStyle@gmail.com',
    description='Omarrrrrv',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Omarail1/omarpoop.git',
    packages=['omarppplp'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License'],
    # install_requires=requires,
)