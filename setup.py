from setuptools import setup, find_packages


setup(
    name='svc',
    description='Image Processing Service',
    classifiers=[
      'Programming Language :: Python',
    ],
    license='Proprietary',
    author='Yevhen Kryvun',
    author_email='yevhen.kryvun@gmail.com',
    url='https://github.com/ukrvassabi/svc-img-processing',

    packages=find_packages(exclude=['tests']),
    namespace_packages=['svc'],
    include_package_data=False,

    install_requires=open('requirements.txt').read().splitlines(),
    tests_require=open('test-requirements.txt').read().splitlines(),
    setup_requires=['setuptools_scm'],
    use_scm_version={'root': '.', 'relative_to': __file__}
)
