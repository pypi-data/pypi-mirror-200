from setuptools import setup, find_packages

setup(
    name = 'kdfba',
    version = '0.2.0',
    keywords='dfba with kinetics',
    install_requires=['cobra>=0.26.0', 'scipy', 'numpy', 'pandas'],
    description = 'dfba algorithm with kinetics to simulate metabolic activities of microbiota',
    long_description = open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license = 'MIT License',
    url = 'https://gitee.com/Xu_Billy/d-fba-package',
    author = 'Xu Billy',
    author_email = 'xu_tian@stu.scu.edu.cn',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
)
