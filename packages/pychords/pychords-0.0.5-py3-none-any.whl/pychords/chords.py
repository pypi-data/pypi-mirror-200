from typing import List, Tuple

from pychords.notes import CN, NO_NOTES, TN
from pychords.chord_types import Spelling, ChordType, find_chord
from pychords.notes import AbstractNote

class AbstractChord:
    """Stores the embodiment of a chord relative to a root note
    """
    def __init__(self, root_note: AbstractNote, chord: ChordType, note_enum) -> None:
        self.root_note = root_note
        self.chord = chord
        self.note_enum = note_enum
    
    def notes(self) -> List:
        """Get the notes of this chord

        return: List of Notes
        """
        # For each note, get the sum of it and the root note
        return [self.note_enum((self.root_note.value + x.value) % NO_NOTES) for x in self.chord.notes]
    
    def spell(self) -> List:
        """Spell the chord, i.e. enumerate the notes

        Example: (for A Major) ["A", "C#", "E"]
        """
        res = []

        # Account for spelling exceptions
        if self.root_note.value in self.chord.exceptions:
            for note in self.notes(): # Just spell everything according to the exception.
                if self.chord.exceptions[self.root_note.value] == Spelling.FLAT:
                    res.append(note.spell_flat())
                else:
                    res.append(note.spell_sharp())

        else:
            for (note, spelling) in zip(self.notes(), self.chord.spelling):
                if spelling == Spelling.FLAT:
                    res.append(note.spell_flat())
                else:
                    res.append(note.spell_sharp())
        return res
    
    def spell_note(self, note: AbstractNote) -> str:
        index = self.notes().index(note)
        return self.spell()[index]
        
    def __str__(self) -> str:
        """Get the string representation of the chord

        Example: (for A Major) "A Major chord with notes A C# E"
        """
        spelling = self.spell()
        return self.spell_note(self.root_note) + " " + self.chord.name + " Chord with notes " + " ".join(spelling)
    
    def short_representation(self) -> str:
        """Get a representation of the chord that consists of only one letter

        Returns:
            str: character
        """
        return self.spell()[0] + self.chord.short

def abstract_chord_from_notes(root_note: AbstractNote, notes: List) -> Tuple[AbstractNote, ChordType]:
    """Get the root note and the chord from a list of notes

    Args:
        root_note (CN): _description_
        notes (List): _description_

    Returns:
        Tuple(AbstractNote, Chord): the parameters needed to create the chord.
    """
    # Subtract the root from everything
    normalized_notes = list(map(lambda x: TN((x.value - root_note.value) % NO_NOTES), notes))
    chord = find_chord(normalized_notes)
    return (root_note, chord)

class ConcreteChord(AbstractChord):
    def __init__(self, root_note: CN, chord: ChordType) -> None:
        super().__init__(root_note, chord, CN)

def concrete_chord_from_notes(root_note: CN, notes: List) -> object:
    """Convert a list of notes into a ConcreteChord

    Args:
        root_note (CN): _description_
        notes (List): _description_

    Returns:
        ConcreteChord: _description_
    """
    (root_note, chord) = abstract_chord_from_notes(root_note, notes)
    return ConcreteChord(root_note, chord)

class TheoreticalChord(AbstractChord):
    def __init__(self, root_note: TN, chord: ChordType) -> None:
        super().__init__(root_note, chord, TN)
    
    def spell(self) -> List:
        """Spell the chord, i.e. enumerate the notes

        Example: (for A Major) ["A, C#, E"]
        """
        return [x.spell_flat() for x in self.notes()]

def theoretical_chord_from_notes(root_note: TN, notes: List) -> object:
    (root_note, chord) = abstract_chord_from_notes(root_note, notes)
    return TheoreticalChord(root_note, chord)