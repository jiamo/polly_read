
import re
import urllib.parse


Max_len = 1450


class Item:

    PAUSE_STRENGTH = ['none', 'x-weak', 'weak', 'medium', 'strong', 'x-strong']

    def __init__(self):
        self.last_inner_seqs = []
        pass

    def add_ms_pause(self, ms):
        self.last_inner_seqs.append("<break time='{}ms'/>".format(ms))
        return self

    def add_strength_pause(self, strength):
        self.last_inner_seqs.append("<break strength='{}'/>".format(strength))
        return self

    def wrap(self):
        pass

    def __str__(self):

        if not self.items and not self.text:
            return ""

        if self.items:
            words_str = " ".join([str(item) for item in self.items])
        elif self.text:
            print(self.text)
            words_str = self.text
        else:
            raise(Exception("should never happend"))

        last_inner_seqs_str = " ".join(self.last_inner_seqs)
        return "{tag} {body} {last_inner_seqs_str} {tag_end}".format(
            tag=self.tag,
            body=words_str,
            last_inner_seqs_str=last_inner_seqs_str,
            tag_end=self.tag_end
        )

    def to_ssml(self):
        # May be we need to know which word should add such
        # these need to parse the text add mark it
        # So it need NLP to processing the text
        return '<speak> <amazon:auto-breaths frequency="low" volume="soft"' \
               ' duration="x-short"> <prosody rate="default"> {} </prosody> ' \
               '</amazon:auto-breaths> </speak>'.format(str(self))


class Word(Item):

    def __init__(self, word):
        super().__init__()
        self.items = [word]
        self.text = None
        self.tag = "<w>"
        self.tag_end = "</w>"


class Sentence(Item):
    def __init__(self, word_list):
        super().__init__()
        self.items = word_list
        self.text = None
        self.tag = "<s>"
        self.tag_end = "</s>"


class Paragraph(Item):

    def __init__(self, sentence_list, break_ms=550):
        super().__init__()
        self.lenth = sum([len(i) for i in sentence_list])
        self.items = sentence_list

        self.text = None
        self.tag = "<p>"
        self.tag_end = "</p>"
        self.add_ms_pause(break_ms)

    @classmethod
    def build_from_text(cls, text):
        text_paragraph = cls([])
        text_paragraph.text = text
        return text_paragraph

    def clean(self):
        self.items = []
        self.lenth = 0

    def add_sentence(self, sentrence):
        len_s = len(sentrence)
        if (len_s + self.lenth) > Max_len:
            return False
        self.items.append(sentrence)
        self.lenth += len_s
        return self

    def is_empty(self):
        return self.lenth == 0
