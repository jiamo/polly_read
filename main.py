import click
import io
from polly_read.txt_to_ssml import TextToMp3, DirTranslate, voices


@click.command()
@click.option('--infile', help='the plain text one line one paragraph')
@click.option('--outfile', help='the output mp3 file')
@click.option('--indir', help='the output mp3 file')
@click.option('--voice', help='the reader name should be {}'.format(str(voices)))
def main(infile, outfile, indir, voice):
    if voice not in voices:
        print("please input voices in {}".format(voices))
        exit(-1)

    if infile and outfile:

        with open(infile, "r", errors='ignore') as f:
            text = f.read()
        io_outfile = io.BytesIO()
        text_to_mp3 = TextToMp3(text, io_outfile, voice)
        text_to_mp3.start()
        with open(outfile, "wb") as f:
            f.write(io_outfile.read())

    elif indir:
        dir_to_mp3 = DirTranslate(indir, voice)
        dir_to_mp3.start()


if __name__ == "__main__":
    main()