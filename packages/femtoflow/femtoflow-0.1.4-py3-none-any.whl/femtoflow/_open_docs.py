import femtoflow
import os
import pathlib

def open_docs():
    femtoflow_path = pathlib.Path(femtoflow.__file__).parent.resolve().parent.resolve()
    doc_path = os.path.join(femtoflow_path, 'docs')
    index_path = os.path.join(doc_path, '_build', 'html', 'index.html')
    cwd = os.getcwd()
    os.system(f'cd {doc_path}; sphinx-apidoc -f . -o .; make html; cd {cwd}; open {index_path}')

open_docs()