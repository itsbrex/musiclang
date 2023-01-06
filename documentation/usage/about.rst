About MusicLang
===============

.. image:: ../images/MusicLang.png
  :width: 400
  :alt: MusicLang logo

The Python framework to write, analyze, transform and predict music.

What is MusicLang ?
--------------------

MusicLang which simply stands for "music language" is a Python framework
that allows composers to write symbolic music in a condensed and high level manner.
This framework is not only another notation software but also
an assistant that is able to automate some tasks that would normally be tedious for a composer.
It is well suited to write new music or to manipulate existing music.

.. note :: This framework supposes that you have some basic knowledge on scales, tonalities and
    roman numeral notation of chords.

How to install
--------------

MusicLang is available on Pypi ::

    pip install musiclang


Or use this repo for the latest version ::

    pip install git+https://github.com/MusicLang/musiclang


Example
-------

Here is a simple example to write a C-major chord in musiclang and save it to midi ::

    from musiclang.library import *

    # Write A C major chord
    score = (I % I.M)(piano__0=s0, piano__1=s2, piano__3=s4)

    # Store it to midi
    score.to_midi('c_major.mid')



Learn MusicLang
---------------

To learn MusicLang we strongly advise to read the :ref:`user-guide`.