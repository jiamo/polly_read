from unittest import TestCase
from polly_read.ssml_builder import (
    Paragraph, Sentence, Word
)
from polly_read.txt_to_ssml import TextToMp3

first = """
    FOR the most wild, yet most homely narrative which I am aboutto pen, I neither expect nor solicit belief. 
    Mad indeed would I be to expect it, in a case where my very senses reject their own evidence.
    Yet, mad am I not -- and very surely do I not dream. 
    But to-morrow I die, and to-day I would unburthen my soul. 
    My immediate purpose is to place before the world, plainly, succinctly, and without comment, a series of mere household events. 
    In their consequences, these events have terrified -- have tortured -- have destroyed me.
    Yet I will not attempt to expound them. 
    To me, they have presented little but Horror -- to many they will seem less terrible than barroques. 
    Hereafter, perhaps, some intellect may be found which will reduce my phantasm to the common-place -- some intellect more calm, more logical, and far less excitable than my own, which will perceive, in the circumstances I detail with awe, nothing more than an ordinary succession of very natural causes and effects.
    """

second = """
    From my infancy I was noted for the docility and humanity of my disposition. 
    My tenderness of heart was even so conspicuous as to make me the jest of my companions. 
    I was especially fond of animals, and was indulged by my parents with a great variety of pets. 
    With these I spent most of my time, and never was so happy as when feeding and caressing them. 
    This peculiarity of character grew with my growth, and, in my manhood, I derived from it one of my principal sources of pleasure. 
    To those who have cherished an affection for a faithful and sagacious dog, I need hardly be at the trouble of explaining the nature or the intensity of the gratification thus derivable. 
    There is something in the unselfish and self-sacrificing love of a brute, which goes directly to the heart of him who has had frequent occasion to test the paltry friendship and gossamer fidelity of mere Man.
"""


class TestToMp3(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_say(self):
        p = Paragraph([Sentence([Word("I"), Word("am")]),
                       Sentence([Word("You"), Word("are")])])
        print(str(p))

