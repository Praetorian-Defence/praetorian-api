from setuptools import setup


def read_files(files):
    data = []
    for file in files:
        with open(file, encoding='utf-8') as f:
            data.append(f.read())
    return "\n".join(data)


meta = {}
with open('praetorian_api/version.py') as f:
    exec(f.read(), meta)

setup(
    name='praetorian-api',
    version=meta['__version__'],
    packages=[
        'praetorian_api',
    ],
    install_requires=[
        'python-dotenv==0.13.*',
        'porcupine-python==0.1.*',
        'django==3.0.*',
        'django-filter==2.*',
        'django-api-forms==0.16.*',
        'django-enum-choices==2.1.*',
        'django-object-checker==1.0.*',
        'django-camel-spitter==0.3.*',
        'django-imap-backend==0.2.*',
        'psycopg2-binary==2.8.*',
        'pycryptodome==3.9.*',
        'pyopenssl==19.1.*',
        'pyotp==2.4.*',
        'qrcode==6.1.*',
        'pillow==7.2.*',
        'sentry-sdk==0.18.*'
    ],
    url='https://github.com/Praetorian-Defence/praetorian-api',
    license='MIT',
    author='Adam Žúrek',
    author_email='adamzurek14@gmail.com',
    description='An information security system providing protection across all major areas of software companies',
    long_description=read_files(['README.md', 'CHANGELOG.md']),
    long_description_content_type='text/markdown',
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
        'Topic :: Security'
    ]
)
