"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
from musiclang.library import *


class Score:
    """Represents a score in musiclang


    """
    def __init__(self, chords=None, config=None, tags=None):
        self.chords = chords
        self.config = config
        if self.chords is None:
            self.chords = []
        if self.config is None:
            self.config = {'annotation': "",
                           "tempo": 120,
                           "pickup": 0,
                           "time_signature": (4, 4)
                           }

        self.tags = set(tags) if tags is not None else set()

    def has_tag(self, tag):
        """
        Check if the tag exists for this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        return tag in self.tags

    def add_tag(self, tag):
        """
        Add a tag to this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        cp = self.copy()
        cp.tags.add(tag)
        return cp

    def add_tags(self, tags):
        """
        Add several tags to the object.
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        score: Score

        """
        cp = self.copy()
        cp.tags = cp.tags.union(set(tags))
        return cp

    def add_tag_children(self, tag):
        """
        Add a tag to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        return Score([c.add_tag(tag) for c in self.chords], tags=self.tags)


    def add_tags_children(self, tags):
        """
        Add several tags to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        score: Score

        """
        return Score([c.add_tags(tags) for c in self.chords], tags=self.tags)

    def remove_tags_children(self, tags):
        """
        Remove several tags to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        score: Score

        """
        return Score([c.remove_tags(tags) for c in self.chords], tags=self.tags)

    def remove_tag_children(self, tag):
        """
        Remove a tag to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        score: Score

        """
        return Score([c.remove_tag(tag) for c in self.chords], tags=self.tags)

    def clear_tags_children(self):
        """
        Clear all tags to each chord composing the score (A score itself don't have tags)
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        score: Score

        """
        return Score([c.clear_tags() for c in self.chords], tags=self.tags)

    def remove_tags(self, tags):
        """
        Remove several tags from the object.
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]

        Returns
        -------
        score: Score


        """
        cp = self.copy()
        cp.tags = cp.tags - set(tags)
        return cp

    def remove_tag(self, tag):
        """
        Remove a tag from this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        cp = self.copy()
        cp.tags.remove(tag)
        return cp

    def clear_tags(self):
        """
        Clear all tags from this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        cp = self.copy()
        cp.tags = set()
        return cp


    def set_amp(self, amp):
        """
        Set the velocity of the notes in the score (between 0 and 120)
        Parameters
        ----------
        amp: int

        Returns
        -------

        """
        return Score([c.set_amp(amp) for c in self.chords], tags=set(self.tags))


    def normalize_instruments(self):
        """
        Get a score with the same instruments on all chords,
        if an instrument is missing on one chord add it with a silence lasting for the chord duration.

        Returns
        -------
        score: Score
        Normalize score
        """
        from musiclang import Silence
        score = None
        instruments = set(self.instruments)
        for chord_raw in self.chords:
            chord = chord_raw.copy()
            missing_instruments = set(instruments) - set(chord.instruments)
            chord_score = chord.score
            for instrument in missing_instruments:
                chord_score[instrument] = Silence(chord.duration)
            score += chord(**chord_score)
        return score

    def remove_silenced_instruments(self):
        """
        Inverse operation of :func:`~Score.normalize_instruments`
        For each chord remove all instruments that are silenced
        Returns
        -------
        score: Score
        """

        score = None
        for chord_raw in self.chords:
            chord = chord_raw.copy()
            chord_score = chord.score

            for instrument in list(chord_score.keys()):
                if all([n.type == 'r' for n in chord_score[instrument]]):
                    del chord_score[instrument]

            score += chord(**chord_score)

        return score

    def replace_instruments(self, **instruments_dict):
        """
        Replace any instrument with another (use full part name (eg: piano__0)

        Parameters
        ----------
        instruments_dict: dict[str, str]
            Dictionary of parts name to replace

        Returns
        -------
        score: Score

        """
        score = None
        instruments_dict = {key: instruments_dict[key] if key in instruments_dict.keys() else key for key in self.parts}
        for chord in self.chords:
            new_chord_dict = {}
            for ins_name, new_ins_name in instruments_dict.items():
                if ins_name in chord.score.keys():
                    new_chord_dict[new_ins_name] = chord.score[ins_name]
            score += chord(**new_chord_dict)

        return score


    def clean(self):
        return self.to_drum().decompose_duration()

    def to_drum(self):
        return Score([chord.to_drum() for chord in self.chords], tags=set(self.tags))

    def to_chords(self):
        """ """
        res = [chord.to_chord() for chord in self.chords]
        return res

    def copy(self):
        """
        Copy the score
        """
        return Score([c.copy() for c in self.chords], config=self.config.copy(), tags=set(self.tags))

    def o(self, val):
        """
        Apply octave to the score.

        Parameters
        ----------
        val : int
            Nb octave to transpose
            

        Returns
        -------
        score: Score
            Octaved score

        """
        return Score([c.o_melody(val) for c in self], config=self.config.copy(), tags=self.tags)

    def __add__(self, other):
        """
        Add another score, or a chord to the current score
        Returns A copy of the score

        Parameters
        ----------
        other: Store or Chord

        Returns
        -------
        score: Score

        """

        from .chord import Chord
        if other is None:
            return self.copy()
        if isinstance(other, Chord):
            return Score(self.copy().chords + [other], config=self.config.copy(), tags=self.tags)
        if isinstance(other, Score):
            return Score(self.copy().chords + other.copy().chords, config=self.config.copy(), tags=self.tags.union(other.tags))
        else:
            raise Exception('Cannot add to Score if not Chord or Score')

    def __iter__(self):
        return self.chords.__iter__()

    def __and__(self, other):
        if isinstance(other, int):
            return Score([c & other for c in self.chords], tags=self.tags)
        else:
            raise Exception(f'Not compatible type with & {other.__class__}')


    @property
    def parts(self):
        return self.instruments

    @property
    def instruments(self):
        """

        Parameters
        ----------

        Returns
        -------
        type
            :return:

        """
        result = []
        for chord in self:
            insts = list(chord.score.keys())
            result += insts
            result = list(set(result))

        return list(sorted(result, key=lambda x: (x.split('__')[0], int(x.split('__')[1]))))


    def octaver(self, **instruments_octaves):
        """
        Transpose down octave per instrument


        Parameters
        ----------
        instruments_octaves: **keywords
                key : instrument_name, val:

        Examples
        --------



        Returns
        -------
        """
        score = None
        for chord in self:
            score += chord(**{instrument: melody.o(instruments_octaves.get(instrument, 0)) for instrument, melody in chord.items()})

        return score


    def apply(self, keep_durations=True, **melodies):
        if keep_durations:
            return Score([c(**melodies).augment(c.duration) for c in self.chords])
        else:
            return Score([c(**melodies) for c in self.chords])

    def to_voicing(self, nb_voices=4, instruments=None):
        """Convert score to a four voice voicing using the extensions provided in the chord.

        It will remove the existing scores of each chord and create the associated voicings

        Parameters
        ----------
        instruments : None or List[str] (Default value = ['piano__0', 'piano__1', 'piano__2', 'piano__3'])
                      The list of instruments used to create the voicings.

        Returns
        -------

        score: Score
               The score with voicings corresponding to chords

        """
        score = None
        for chord in self:
            score += chord.to_voicing(nb_voices=nb_voices, instruments=instruments)

        return score

    def show(self, *args, **kwargs):
        """Wrapper to the music21 show method
        :return:

        Parameters
        ----------
        *args :
            
        **kwargs :
            

        Returns
        -------

        """
        import music21
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as di:
            m21_score = self.to_music21(**kwargs)
            return m21_score.show(*args)


    def __setitem__(self, key, value):
        return self.chords.__setitem__(key, value)

    def __getitem__(self, item):
        """
        If str return a score with only this voice
        else returns item getter of the list of chords and convert it back to a score
        """
        from .note import Silence
        from .chord import Chord
        if isinstance(item, str):
            new_score = None
            for chord in self:
                if item in chord.score.keys():
                    new_score += chord(**{item: chord.score[item]})
                else:
                    new_score += chord(**{item: Silence(chord.duration)})
            return new_score
        elif isinstance(item, list):
            new_score = None
            for chord in self:
                chord_score = {}
                for it in item:
                    if it in chord.score.keys():
                        chord_score[it] = chord.score[it]
                    else:
                        chord_score[it] = Silence(chord.duration)
                new_score += chord(**chord_score)

            return new_score
        else:
            chords = self.chords.__getitem__(item)
            if isinstance(chords, Chord):
                return chords
            return sum(chords, None)

    def put_on_same_chord(self):
        """Take the first chord as reference,
        Put everything into the first chord preserving the note value (It will change the piece to a static harmony)

        Parameters
        ----------
        score : Score
                Input score


        Returns
        -------
        score: Score
               Score containing one chord with all the melodies

        Examples
        --------

        >>> from musiclang.library import *
        >>> score = (I % I.m)(piano__0=s0) + (V % I.m)(piano__0=s2)
        >>> score.put_on_same_chord()
        (I % I.m)(piano__0=s0 + s2)

        """
        from .time_utils import put_on_same_chord
        return put_on_same_chord(self)

    def project_on_score(self, score2, keep_pitch=False, voice_leading=True, keep_score=False,
                         repeat_to_duration=False, allow_override=False):
        """Project harmonically the current score onto the score2.
        The score2 notes will disappear, only keeping the current score with the harmony of score2
        Can either project by complete diatonic transposition or trying to move as little as possible the notes
        (voice_leading=True)

        Algorithm : For each chord of score2 : get chords that belongs to score1 and reproject on chord of score2

        Parameters
        ----------
        score : Score
                Score to project on the chords of score2
        score2 : Score
            Score that contains the harmony
        voice_leading: boolean (default=True)
            If true, we try to move the notes as little as possible
        voice_leading : boolean (default=True)
            If True try to move the notes as little as possible (Default value = True)
        repeat_to_duration: boolean (default=False)
            If True then Repeat the score to fit the duration of score2
        allow_override: boolean (default=False)
            In case keep_score is True should we allow existence of intersection of voices between self and score2 ?
            If True score2 parts that exists in self will be replaced by projected parts of self. Otherwise raise an Exception
        Returns
        -------
        new_score: Score
                  The score projected on score2 chord progression. It will fit the minimal duration of both scores

        Examples
        --------

        >>> from musiclang.library import *
        >>> score1 = (I % I.m)(piano__0=s0.e) + (V % I.m)(piano__0=s2.e)
        >>> score2 = (II % III.m)(piano__0=s0.e + s0.e)
        >>> score1.project_on_score(score2, voice_leading=False)
        (II % III.m)(piano__0=s0.e + s2.e)

        """
        # Algo : For each chord of score2 : get chords that belongs to score1 and reproject on chord of score2
        from .time_utils import project_on_score
        from musiclang.transform.composing import project_on_score_keep_notes

        if repeat_to_duration and self.duration < score2.duration:
            diff_duration = (score2.duration // self.duration) + 1
            to_project = self * diff_duration
        else:
            to_project = self

        if keep_pitch:
            to_project = self.to_absolute_note()

        if voice_leading:
            result_score = project_on_score_keep_notes(to_project.to_score(), score2.to_score())
        else:
            result_score = project_on_score(to_project.to_score(), score2.to_score(), keep_score=False)

        if keep_score:
            if not allow_override and len(set(result_score.parts).intersection(score2.parts)) != 0:
                raise Exception('If keep_score flag is True, parts should be differents between the scores')

            result_score = sum([c1(**{**c2.score, **c1.score}) for c1, c2 in zip(result_score.chords, score2.chords)], None)

        return result_score

    def to_absolute_note(self):
        return Score([chord.to_absolute_note() for chord in self.chords], tags=self.tags)


    def get_chord_between(self, chord, start, end):
        """

        Parameters
        ----------
        chord :
            
        start :
            
        end :
            

        Returns
        -------

        """
        from .time_utils import get_chord_between
        return get_chord_between(chord, start, end)

    @property
    def pedal_each_chord(self):
        return Score([c.pedal for c in self.chords], tags=set(self.tags))

    def doubling(self, **args):
        new_score = None
        for chord in self.chords:
            score = chord.copy().score
            for part, new_parts in args.items():
                if isinstance(new_parts, str):
                    new_parts = [new_parts]
                for new_part in new_parts:
                    if part in score.keys():
                        score[new_part] = score[part].copy()
            new_score += chord(**score)

        return new_score

    def get_score_between(self, start=None, end=None):
        """
        Get the score between start and end time.

        Parameters
        ----------
        start :
             (Default value = None)
        end :
             (Default value = None)

        Returns
        -------

        """
        from .time_utils import get_score_between
        return get_score_between(self, start, end)

    def reduce(self, n_voices=4, start_low=False, instruments=None):
        """
        Reduce the score to n_voices

        Parameters
        ----------
        n_voices : int, (Default value = 4)
                   Number of voices in the reduction
        start_low : bool (Default value = False)
                    If true the first voice in the reduction will be the bass, else the soprano
        instruments : List[str] or None (Default value = None)
                      Name of the voices in the reduction
        Returns
        -------
        score : Score
                The reduced score

        Examples
        --------

        >>> from musiclang.library import *
        >>> score = (I % I.M)(piano=[s0, s2, s4]) + (V % I.M)(piano=[s0, s2, s4])
        >>> score.reduce(n_voices=2, start_low=False, instruments=['cello__0', 'violin__0'])
        (I % I.M)(
            cello__0=s0,
            violin__0=s4)+
        (V % I.M)(
            cello__0=s0,
            violin__0=s4)

        """
        from .arrange_utils import reduce
        return reduce(self, n_voices=n_voices, start_low=start_low, instruments=instruments)

    def to_pickle(self, filepath):
        """
        Save the score into a pickle file

        Parameters
        ----------
        filepath : str
                   Filepath on which to save the score

        """
        import pickle
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def from_annotation_file(cls, file):
        with open(file, 'r') as f:
            text = f.read()
        return Score.from_annotation(text)

    @classmethod
    def from_annotation(cls, text):
        from musiclang.analyze import ScoreFormatter
        return ScoreFormatter(text).parse()


    @classmethod
    def from_midi(cls, filename):
        """
        Load a midi score into musiclang

        .. warning:: This step can take some time depending on the length of the file

        Parameters
        ----------
        filename : str
                   Filepath of the file

        Returns
        -------
        score: Score
               The loaded score

        """
        from musiclang.analyze import parse_to_musiclang
        score, config = parse_to_musiclang(filename)
        score.config = config
        return score

    def to_extension_note(self):
        return Score([chord.to_extension_note() for chord in self.chords], tags=set(self.tags))

    def to_chord_note(self):
        return Score([chord.to_chord_note() for chord in self.chords], tags=set(self.tags))

    def to_standard_note(self):
        return Score([chord.to_standard_note() for chord in self.chords], tags=set(self.tags))


    @classmethod
    def from_xml(cls, filename):
        """
        Load a musicxml score into musiclang

        .. warning:: This step can take some time depending on the length of the file


        Parameters
        ----------
        filename : str
                   Filepath of the file
            

        Returns
        -------

        score: Score
               The loaded score

        """
        from musiclang.analyze import parse_to_musiclang
        score, config = parse_to_musiclang(filename)
        score.config.update(config)
        return score

    def decompose_duration(self):
        """
        Decompose the duration in a note + continuations. It recursively call
        :func:`~Note.decompose_duration()`
        """
        return Score([chord.decompose_duration() for chord in self.chords], tags=self.tags)

    def to_score(self, copy=True):
        """ """
        if not copy:
            return self
        else:
            return self.copy()


    @classmethod
    def from_str(cls, s):
        from musiclang.library import I, II, III, IV, V, VI, VII
        from musiclang.library import s0, s1, s2, s3, s4, s5, s6
        from musiclang.library import h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11
        from musiclang.library import su0, su1, su2, su3, su4, su5, su6
        from musiclang.library import hu0, hu1, hu2, hu3, hu4, hu5, hu6, hu7, hu8, hu9, hu10, hu11
        from musiclang.library import sd0, sd1, sd2, sd3, sd4, sd5, sd6
        from musiclang.library import hd0, hd1, hd2, hd3, hd4, hd5, hd6, hd7, hd8, hd9, hd10, hd11
        return eval(s.replace('\n', ''))

    @classmethod
    def from_sequence(cls, sequence, **kwargs):
        """

        Parameters
        ----------
        sequence :
            
        **kwargs :
            

        Returns
        -------

        """
        from .sequence.sequence import sequence_to_score
        return sequence_to_score(sequence, **kwargs)

    def to_sequence(self, **kwargs):
        """
        Convert
        Parameters
        ----------
        **kwargs :
            

        Returns
        -------

        """
        from .sequence.sequence import score_to_sequence
        return score_to_sequence(self, **kwargs)


    @classmethod
    def from_pickle(cls, filepath):
        """

        Parameters
        ----------
        filepath :
            

        Returns
        -------

        """
        import pickle
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return data

    def __eq__(self, other):
        from .chord import Chord
        if isinstance(other, Chord):
            return self == Score([other], config=self.config.copy())
        if not isinstance(other, Score):
            return False
        elif len(other.chords) != len(self.chords):
            return False
        else:
            return all([c1 == c2 for c1, c2 in zip(self.chords, other.chords)])

    def __getattr__(self, item):
        chords = self.copy()
        chords.chords = [getattr(s, item) for s in self.chords]
        return chords

    def __mod__(self, other):
        from .tonality import Tonality
        if isinstance(other, Tonality):
            return Score([c % other for c in self.chords], config=self.config.copy(), tags=self.tags)
        else:
            raise Exception('Following % should be a Tonality')

    def remove_accidents(self):
        return Score([chord.remove_accidents() for chord in self.chords], tags=set(self.tags))


    def __mul__(self, other):
        """
        If other is Integer, repeat the note other times
        """
        if isinstance(other, int):
            return sum([self.copy() for i in range(other)], None)
        else:
            raise Exception('Cannot multiply Score and ' + str(type(other)))

    def __radd__(self, other):
        if other is None:
            return self.copy()

    def __repr__(self):
        return '+ \n'.join([str(chord) for chord in self.chords])

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d


    @property
    def duration(self):
        """ """
        return sum([c.duration for c in self.chords])

    def to_code(self, **kwargs):
        """Export the chord serie as a string representing valid python code that recreates the score
        :return:

        Parameters
        ----------
        **kwargs :
            

        Returns
        -------

        """
        from .out.to_code import chord_serie_to_code

        code = chord_serie_to_code(self, **kwargs)
        return code

    def to_code_file(self, filepath, **kwargs):
        """Export the chord serie as a file representing valid python code that recreates the score

        Parameters
        ----------
        filepath :
            return:
        **kwargs :
            

        Returns
        -------

        """
        code = self.to_code(**kwargs)
        with open(filepath, 'w') as f:
            f.write(code)

    def to_musicxml(self, filepath, signature=(4, 4), tonality=None, tempo=120, no_repeat=False, **kwargs):
        """
        Transform a musiclang score into a musicxml file, readable by all the main notation software (musescore, finale ...)

        Parameters
        ----------
        score: Score
                MusicLang score to transform
        filepath: str
                Filepath of the musicxml file
        signature: tuple (nom, den)
                Time signature of the piece
        tempo: int
                Tempo of the piece
        tonality: Tonality
                Tonality of the piece if applicable
        title: str
            Title of the piece

        """
        # Convert score to midi
        from .out.to_mxl import score_to_mxl

        return score_to_mxl(self, filepath, signature=signature, tonality=tonality, tempo=tempo, no_repeat=no_repeat, **kwargs)

    def to_music21(self, signature=(4, 4), tonality=None, tempo=120, **kwargs):
        """
        Transform a musiclang score into a Music21 score
        Parameters
        ----------
        score: Score
                MusicLang score to transform
        signature: tuple (nom, den)
                Time signature of the piece
        tempo: int
                Tempo of the piece
        tonality: Tonality
                Tonality of the piece if applicable
        title: str
            Title of the piece

        Returns
        -------
        m21_score: music21.Score
            Score transformed into a music21 object

        """
        from .out.to_mxl import score_to_music_21
        return score_to_music_21(self, signature=signature, tonality=tonality, tempo=tempo, **kwargs)

    def to_midi(self, filepath, **kwargs):
        """
        Save the score to midi

        Parameters
        ----------
        filepath :
            
        **kwargs :
            

        Returns
        -------

        """
        # Convert score to midi
        from .out.to_midi import score_to_midi

        return score_to_midi(self, filepath, **kwargs)

