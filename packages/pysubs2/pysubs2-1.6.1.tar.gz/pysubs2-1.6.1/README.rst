pysubs2
=======


.. image:: https://img.shields.io/github/actions/workflow/status/tkarabela/pysubs2/main.yml?branch=master
    :alt: pysubs2 build master branch
    :target: https://github.com/tkarabela/pysubs2/actions
.. image:: https://img.shields.io/codecov/c/github/tkarabela/pysubs2
    :alt: pysubs2 test code coverage
    :target: https://app.codecov.io/github/tkarabela/pysubs2
.. image:: http://www.mypy-lang.org/static/mypy_badge.svg
    :alt: MyPy checked
    :target: https://github.com/tkarabela/pysubs2/actions
.. image:: https://img.shields.io/pypi/v/pysubs2.svg?style=flat-square
    :alt: PyPI - Version
    :target: https://pypi.org/project/pysubs2/
.. image:: https://img.shields.io/pypi/status/pysubs2.svg?style=flat-square
    :alt: PyPI - Status
    :target: https://pypi.org/project/pysubs2/
.. image:: https://img.shields.io/pypi/pyversions/pysubs2.svg?style=flat-square
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/pysubs2/
.. image:: https://img.shields.io/pypi/l/pysubs2.svg?style=flat-square
    :alt: PyPI - License
    :target: LICENSE.txt


pysubs2 is a Python library for editing subtitle files.
It’s based on *SubStation Alpha*, the native format of
`Aegisub <http://www.aegisub.org/>`_; it also supports *SubRip (SRT)*,
*MicroDVD*, *MPL2*, *TMP* and *WebVTT* formats and *OpenAI Whisper* captions.

There is a small CLI tool for batch conversion and retiming.

.. code:: bash

    $ pip install pysubs2
    $ pysubs2 --shift 0.3s *.srt
    $ pysubs2 --to srt *.ass

.. code:: python

    import pysubs2
    subs = pysubs2.load("my_subtitles.ass", encoding="utf-8")
    subs.shift(s=2.5)
    for line in subs:
        line.text = "{\\be1}" + line.text
    subs.save("my_subtitles_edited.ass")

To learn more, please `see the documentation <http://pysubs2.readthedocs.io>`_.
If you'd like to contribute, see `CONTRIBUTING.md <CONTRIBUTING.md>`_.

pysubs2 is licensed under the MIT license (see `LICENSE.txt <LICENSE.txt>`_).
