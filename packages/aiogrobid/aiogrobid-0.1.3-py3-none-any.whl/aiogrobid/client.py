from aiobaseclient import BaseClient
from lxml import etree

from .exceptions import BadRequestError


class GrobidClient(BaseClient):
    def _get_text_for_one(self, root, name):
        r = root.find(name)
        return self._get_text(r)

    def _get_text(self, node):
        result = ''
        if node is not None:
            if node.text:
                result = node.text.strip()
            for child in node:
                if child is not None and child.tail is not None and child.tail.strip():
                    result += ' ' + child.tail.strip()
        return result

    def _extract(self, node):
        result = ''
        for possibly_div in node.getchildren():
            if possibly_div.tag == '{http://www.tei-c.org/ns/1.0}div':
                for child in possibly_div.getchildren():
                    if child.tag == '{http://www.tei-c.org/ns/1.0}head':
                        result += ('\n\n' + self._get_text(child) + '\n')
                    if child.tag == '{http://www.tei-c.org/ns/1.0}p':
                        result += self._get_text(child)
        return result.strip()

    async def process_fulltext_document(self, pdf_file):
        return await self.post(
            '/api/processFulltextDocument',
            data={
                'input': pdf_file,
            },
        )

    async def response_processor(self, response):
        content = await response.read()
        if response.status != 200:
            raise BadRequestError(status=response.status)
        try:
            root = etree.XML(content)
        except etree.XMLSyntaxError as e:
            raise BadRequestError(nested_error=e)
        return {
            'doi': self._get_text_for_one(root, ".//{http://www.tei-c.org/ns/1.0}idno[@type='DOI']"),
            'title': self._get_text_for_one(root, ".//{http://www.tei-c.org/ns/1.0}title[@level='a'][@type='main']"),
            'abstract': self._extract(root.find(".//{http://www.tei-c.org/ns/1.0}abstract")),
            'body': self._extract(root.find(".//{http://www.tei-c.org/ns/1.0}body")),
        }
