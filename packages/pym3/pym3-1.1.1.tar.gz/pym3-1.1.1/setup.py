from setuptools import setup
def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

setup(
    name='pym3',
    version='1.1.1',
    description='Python Version Management, Simplified. Wrap `pipx` and `poetry` Tools',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='tomas',
    author_email='',
    license='MIT',
    zip_safe=False,
    scripts=[
        'bin/p',
        'bin/py3',
    ],
   classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Unix Shell',
        'Topic :: System :: Shells',
        'Topic :: Utilities'
    ],
)
