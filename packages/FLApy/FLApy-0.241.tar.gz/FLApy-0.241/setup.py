from setuptools import setup, find_packages


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='FLApy',
    version='0.241',
    description='Forest Light availability heterogeneity Analysis in Python',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author='Bin Wang',
    author_email='wb931022@hotmail.com',
    url='https://github.com/niB-gnaW/FLApy',
    packages=find_packages(),
    py_modules=['FLApy.__init__', 'FLApy.DataManagement', 'FLApy.LAcalculator', 'FLApy.LAHanalysis', 'FLApy.Visualization'],
    classifiers=['Programming Language :: Python :: 3.7', 'License :: OSI Approved :: MIT License', 'Operating System :: OS Independent',],
    python_requires='>=3.7',
    install_requires=['numpy==1.21.2',
                      'scipy==1.6.0',
                      'matplotlib==3.7.1',
                      'open3d==0.12.0',
                      'pyvista==0.33.3',
                      'PVGeo==2.1.0',
                      'laspy==1.7.0',
                      'pandas==1.3.2',
                      'tqdm==4.62.2',
                      'p_tqdm==1.4.0',
                      'miniball==1.1.0',
                      'rasterio~=1.2.6',
                      'xarray==0.19.0'],)

