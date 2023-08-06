from x2cdict import VocabDict, PhraseDict
import click

@click.command()
@click.option("--word", help="Specify the word to look up", prompt="word")
@click.option("--pos", help="Specify PoS of the word", default=None)
@click.option("--fromlang", help="Specify the language of the word", prompt="translate from")
@click.option("--tolang", help="Specify the language the word to be translated into", prompt="translate to", default="cn")
@click.option("--external", help="Whether using the external source", prompt="using external source", type=bool, default=True)
def search_vocab(word, pos, fromlang, tolang, external):
  vd = VocabDict(fromlang, tolang)
  r = vd.search(word, pos, external)
  print(r)


@click.command()
@click.option("--word", help="Specify the word to look up", prompt="word")
@click.option("--fromlang", help="Specify the language of the word", prompt="translate from")
@click.option("--tolang", help="Specify the language the word to be translated into", prompt="translate to", default="cn")
@click.option("--external", help="Whether using the external source", prompt="using external source", type=bool, default=True)
def search_vocab_without_pos(word, fromlang, tolang, external):
  vd = VocabDict(fromlang, tolang)
  r = vd.search_without_pos(word, external)
  print(r)


@click.command()
@click.option("--phrase", help="Specify the phrase to look up", prompt="phrase")
@click.option("--fromlang", help="Specify the language of the word", prompt="translate from")
@click.option("--tolang", help="Specify the language the word to be translated into", prompt="translate to", default="cn")
def search_phrase(phrase, fromlang, tolang):
  vd = PhraseDict(fromlang, tolang)
  r = vd.search(phrase)
  print(r)

