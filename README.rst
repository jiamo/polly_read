=====
polly_read
=====


.. image:: https://img.shields.io/pypi/v/polly_read.svg
        :target: https://pypi.python.org/pypi/polly_read

.. image:: https://img.shields.io/travis/jiamo/polly_read.svg
        :target: https://travis-ci.org/jiamo/polly_read

.. image:: https://readthedocs.org/projects/polly_read/badge/?version=latest
        :target: https://polly_read.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/jiamo/polly_read/shield.svg
     :target: https://pyup.io/repos/github/jiamo/polly_read/
     :alt: Updates



* Free software: MIT license
* Documentation: https://polly_read.readthedocs.io.
* inspire ref: https://github.com/agentzh/amazon-polly-batch but pure python


example
--------
* file or dir tranlate ::

    python main.py --infile test.txt --outfile test.mp3 --voice Joey
    python main.py --indir testdir --voice Joey # this will create mp3 indir


* in memory translate and put file to s3 ::

    just use `io.BytesIO`
