from setuptools import setup, find_packages

setup(
  name='vipera',
  version='0.1.0',
  author='Renan Araújo',
  author_email='asrenan@outlook.com.br',
  description='A CLI tool for PDF manipulation',
  packages=find_packages(),
  entry_points={
      'console_scripts': [
          'vibora = vibora.main:main',
      ],
  },
  classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
  ],
  keywords='pdf conversion manipulation',
  install_requires=[
      'pdf2image',
      'PyPDF2',
      'fitz',
      'pdf2image',
      'Pillow',
      'PDFNetPython3',
  ],
)
