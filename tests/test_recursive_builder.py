from unittest import TestCase
from polly_read.ssml_builder import (
    Paragraph, Sentence, Word
)


class TestPySSMLNestBuilder(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_say(self):
        p = Paragraph(
            [Sentence([Word("I"), Word("am")]).add_ms_pause(1000).add_strength_pause("x-strong"),
             Sentence([Word("You"), Word("are")]).add_ms_pause(1000)])
        print(p.to_ssml())

    def test_paragraph(self):
        p = Paragraph.build_from_text("hello world")
        print(p.text)
        print(p.to_ssml())
