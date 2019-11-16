from git import Repo
import markdown
from datetime import datetime
from diff_match_patch import diff_match_patch

REPO_PATH = 'data/constitucion_chile'
BUILT_FILES_PATH = 'data/built_pages/'
IGNORED_FILES = [
    'README.md',
    '.gitignore',
    '.vscode'
]

def filter_content_files(blob):
    return blob.name not in IGNORED_FILES

def markdown2html(markdown_contents):
    return markdown.markdown(markdown_contents)

def get_sorted_blobs_from_commit(commit):
    blobs = list(filter(filter_content_files, commit.tree.blobs))
    blobs.sort(key=lambda b: b.name)
    return blobs

def concatenate_blobs(blobs):
    concatenated = ''
    for blob in blobs:
        concatenated += '\n'
        concatenated += str(blob.data_stream.read().decode('utf-8'))
    return concatenated

def write_to_path(content, filepath):
    f = open(filepath, 'w')
    f.write(content)
    f.close()

def get_sorted_commits():
    repo = Repo(REPO_PATH)
    commits = list(repo.iter_commits('master', max_count=50))
    commits.reverse()
    return commits

def diff_contents(previous, current):
    dmp = diff_match_patch()
    diff = dmp.diff_main(previous, current)
    dmp.diff_cleanupSemantic(diff)
    return diff

def diff_as_html_files(previous, current):
    previous_html = markdown2html(previous)
    current_html = markdown2html(current)
    diff = diff_contents(previous_html, current_html)
    return concat_diffed(diff)

def concat_diffed(diffed):
    result = ''
    for element in diffed:
        status = element[0] 
        content = element[1]
        if status == -1:
            result += f'\n<Del>{content}</Del>'
        elif status == 0:
            result += content
        elif status == 1:
            result += f'\n<Ins>{content}</Ins>'
    return result




if __name__=='__main__':
    commits = get_sorted_commits()
    previous_commit_content = None
    for commit in commits:
        date = datetime.fromtimestamp(commit.authored_date).date()
        blobs = get_sorted_blobs_from_commit(commit)
        current_commit_content = concatenate_blobs(blobs)

        html_result = None
        if previous_commit_content is None:
            html_result = markdown2html(current_commit_content)
        else:
            html_result = diff_as_html_files(previous_commit_content, current_commit_content)
        previous_commit_content = current_commit_content

        filepath = BUILT_FILES_PATH + f'{date}.html'
        write_to_path(html_result, filepath)

