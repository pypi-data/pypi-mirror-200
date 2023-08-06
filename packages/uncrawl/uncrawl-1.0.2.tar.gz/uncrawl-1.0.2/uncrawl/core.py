import os
import html
from newspaper import Article


def write_in(file, content, n=2):
    file.write(f"{html.escape(content)}" + ('\n' * n))


def process_article(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article


def write_list(file, title, items):
    write_in(file, f"## {title}")
    if items:
        for item in items[:-1]:
            write_in(file, item)
        write_in(file, items[-1])
    else:
        write_in(file, f"No {title.lower()} found")


def write_article_to_file(file, article: Article):
    sections = [
        ("", article.title),
        ("Authors", article.authors),
        ("Publish Date", [str(article.publish_date)]
         if article.publish_date else []),
        ("Keywords", article.keywords),
        ("Summary", [article.summary]),
        ("Full Content", [article.text]),
    ]

    for title, content in sections:
        if title:
            write_list(file, title, content)
        else:
            write_in(file, f"# {content}")
            print(article.title + ' is ready')


def uncrawl(url, path):
    """
    :type url: str
    :type path: int 
        path with markdown filename
    """
    file_name = path + '.md'
    dir_path = os.path.dirname(file_name)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)

    try:
        with open(file_name, 'w'):
            pass
    except IOError as e:
        print(f"Error creating file '{file_name}': {e}")
        return

    try:
        article = process_article(url)
    except Exception as e:
        print(f"Error processing article from URL '{url}': {e}")
        return

    try:
        with open(file_name, 'a') as file:
            write_article_to_file(file, article)
    except IOError as e:
        print(f"Error appending to file '{file_name}': {e}")
