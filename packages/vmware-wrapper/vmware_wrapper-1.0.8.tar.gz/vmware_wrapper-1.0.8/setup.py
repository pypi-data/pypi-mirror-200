from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()
requirements = ['urllib3==1.26.15', 'requests==2.27.1']

setup(
    name='vmware_wrapper',
    version='1.0.8',
    author='Kanaev Oleg',
    author_email='saga6021@gmail.com',
    description='A package to work with VMware Workstation. Local/vSphere storages',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Oleggg2000/vmware_wrapper',
    keywords=['python', 'vmware', 'vmrest', 'vmrest.cfg', 'VMware', 'VMware Workstation',
              'vsphere-automation-sdk-python', 'vmware sdk'],
    packages=find_packages(),
    dependency_links=['git+https://github.com/vmware/vsphere-automation-sdk-python@v8.0.0.1'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.11',
    ],
)
