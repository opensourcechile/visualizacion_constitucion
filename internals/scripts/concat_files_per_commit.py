from git import Repo
import markdown
from datetime import datetime

REPO_PATH = 'data/constitucion_chile'
IGNORED_FILES = [
    'README.md',
    '.gitignore',
    '.vscode'
]

def filterContentFiles(blob):
    return blob.name not in IGNORED_FILES

def markdown2html(markdown_contents):
    return markdown.markdown(markdown_contents)


if __name__=='__main__':
    repo = Repo(REPO_PATH)
    commits = list(repo.iter_commits('master', max_count=50))
    for commit in commits:
        date = datetime.fromtimestamp(commit.authored_date).date()
        filepath = f'data/built_pages/{date}.html'
        blobs = list(filter(filterContentFiles, commit.tree.blobs))
        blobs.sort(key=lambda b: b.name)
        concatenated = ''
        for blob in blobs:
            concatenated += '\n'
            concatenated += str(blob.data_stream.read().decode('utf-8'))
        f = open(filepath, 'w')
        f.write(markdown2html(concatenated))
        f.close()


