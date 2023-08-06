import os
import time
from dataclasses    import dataclass
from docxtpl        import DocxTemplate

from typing         import Dict


@dataclass
class DocHandle():
    f_name : str


class Docgen():
    def __init__(self, docs : Dict, config):
        self.docs_info = [
            { 'tag' : doc['tag'], 'name' : doc['name'] } for
                doc in docs.values()
        ]

        self.templates_dir  = config.MAXDMG_DOCGEN_TEMPLATES_DIR
        if not os.path.isdir(self.templates_dir):
            raise RuntimeError(f"maxdmg-docgen -- {self.templates_dir} is not a templates dir or does not exist.")

        self.tmp_dir        = config.MAXDMG_DOCGEN_TMP_DIR
        if not os.path.isdir(self.tmp_dir):
            raise RuntimeError(f"maxdmg-docgen -- {self.tmp_dir} is not a tmp dir or does not exist.")

    def MakeDocument(self, tags):
        """
        file_dir = os.path.dirname(os.path.realpath(__file__))
        tmp_dir  = os.path.join(file_dir, 'tmp')
        """
        f_name   = os.path.join(self.tmp_dir, 
                                time.strftime("%Y%m%d%H%M%S")) + ".docx"
        self.__MakeDocumentJinja(f_name, tags)
        return DocHandle(f_name=f_name)

    def DeleteDocument(self, doc_name):
        try:
            os.remove(doc_name)
        except FileNotFoundError:
            pass

    def __MakeDocumentJinja(self, f_name, tags):
        doc = self.__GetDoc(tags)
        if not doc:
            raise RuntimeError(f"maxdmg-docgen -- no {f_name} doc found")
        doc.render(tags)
        doc.save(f_name)

    def __GetDoc(self, tags):
        """
        file_dir        = os.path.dirname(os.path.realpath(__file__))
        templates_dir   = os.path.join(file_dir, 'templates')
        """

        for doc in self.docs_info:
            if tags.get(doc['tag'], None):
                return DocxTemplate(
                    os.path.join(self.templates_dir, doc['name']))
        return None

