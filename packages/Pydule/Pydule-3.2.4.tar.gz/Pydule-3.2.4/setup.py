from setuptools import setup
import setuptools

with open('README.md','r') as fh:
	long_description = fh.read()

setup(
	name='Pydule',
	version='3.2.4',
	description="Download Audio From Youtube Video or Video with Audio,Play Songs,Create Qrcode,Translate a Sentence to Other Language and more..",
	author='D.Tamil Mutharasan',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=setuptools.find_packages(),
	keywords=['python','PyDule','Module','Pydule','pydule','matrix','qrcode','youtube','weather','list','tuple','set','dictionary','clear','color','pick_color','open','app','search','play','mp3','song','restart','system','shutdown','date','time','text_to_speech','text','speech'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Intended Audience :: Education",
		"Operating System :: Microsoft :: Windows :: Windows 10",
		"Development Status :: 5 - Production/Stable"
	],
	python_requires='>=3.10.7',
	py_modules=['Pydule'],
	package_dir={'':'src'},
	install_requires=[
		'beautifulsoup4',
		'pyttsx3',
		'pywhatkit',
		'playsound',
		'datetime',
		'requests',
		'AppOpener',
		'deep_translator',
		'qrcode',
		'pytube',
		'numpy'
	]

)