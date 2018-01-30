import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from .ssml_builder import Paragraph
import argparse
import os
import io
import sys
import textwrap
import glob

polly = boto3.client("polly")

voices = ['Geraint', 'Gwyneth', 'Mads', 'Naja',
          'Hans', 'Marlene', 'Nicole', 'Russell', 'Amy', 'Brian', 'Emma',
          'Raveena', 'Ivy', 'Joanna', 'Joey', 'Justin', 'Kendra', 'Kimberly',
          'Matthew', 'Salli', 'Conchita', 'Enrique', 'Miguel', 'Penelope',
          'Chantal', 'Celine', 'Mathieu', 'Dora', 'Karl', 'Carla', 'Giorgio',
          'Mizuki', 'Liv', 'Lotte', 'Ruben', 'Ewa', 'Jacek', 'Jan', 'Maja',
          'Ricardo', 'Vitoria', 'Cristiano', 'Ines', 'Carmen', 'Maxim',
          'Tatyana', 'Astrid', 'Filiz', 'Vicki', 'Takumi', 'Seoyeon', 'Aditi']
default_voice = 'Joey'


class TextToMp3:

    def __init__(self, text, out_bytesio, voice=default_voice):
        """
        The main reason using io.BytesIO here is for aws service
        and save directly to mp3 in s3
        """
        self.out_bytesio = out_bytesio
        self.rules = {}
        self.voice = voice
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace("\n", "")  # only remove \n in paragraph
        self.pieces = text.split("\n")

    def start(self):
        for piece in self.pieces:
            self.add_paragraph(piece)
        self.close()

    def close(self):
        self.out_bytesio.seek(0)

    def add_paragraph(self, text):

        # build new p
        if len(text) >= 1500:  # the TextLengthExceededException of polly
            # split into different paragraph
            sentences = text.split(".")
            print(sentences)
            p = Paragraph([])

            while sentences:
                # it is strange add . but it need
                sentence = sentences.pop(0)
                sentence = sentence.strip(" ")
                if not sentence:
                    continue
                if p.add_sentence(sentence + "."):
                    continue
                else:
                    if not p.is_empty():
                        self.translate(p.to_ssml())
                        p.clean()
                        # need handle the failed sentence
                        # print("failed sentence {}".format(sentence))
                        sentences.insert(0, sentence)
                        continue
                    else:
                        # which mean the sentence it self has 1500
                        # in this case we need human being to see it
                        print("This is sentence is too much long:\n{}".format(
                            sentence))
                        sys.exit()
            if not p.is_empty():
                self.translate(p.to_ssml())
        else:
            p = Paragraph.build_from_text(text)
            self.translate(p.to_ssml())

    def translate(self, ssml_string):
        print("translate {} : {}".format(len(ssml_string), ssml_string))
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(
                Text=ssml_string,
                TextType="ssml",
                OutputFormat="mp3",
                VoiceId=self.voice)
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

        # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                try:
                    self.out_bytesio.write(stream.read())
                except IOError as error:
                    print(error)
                    sys.exit(-1)

        else:
            print("Could not stream audio")
            sys.exit(-1)

        print("translate finish")


class DirTranslate():
    def __init__(self, indir, voice):
        self.indir = indir
        self.voice = voice

    def start(self):
        txts = glob.glob(self.indir + "/*.txt")
        txts = sorted(txts)
        for txt in txts:
            print("handing txt {}".format(txt))
            with open(txt, "r", errors='ignore') as f:
                text = f.read()
            mp3 = txt[:-3] + "mp3"
            io_outfile = io.BytesIO()
            txt2mp3 = TextToMp3(text, io_outfile, self.voice)
            txt2mp3.start()
            with open(mp3, "wb") as f:
                f.write(io_outfile.read())
