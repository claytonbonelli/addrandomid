#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
from bs4.element import Tag
import uuid
import os


class AddRandomIdCommand:
    """
    Sometimes when we develop our HTML pages, we forget to include the unique identifiers (IDs) in our tags. 
    Later we realize that when we need these identifiers, for example when we use automated testing tools, 
    we must manually include those same IDs in each of the tags that will be tested, which is a tedious task. 
    To avoid this manual work, this tool was developed with the mission of including unique identifiers (IDs) 
    in all HTML tags that exist in the files.

    The operation is very simple, you indicate the base directory where the HTML files can be found and recursively 
    (configurable) each subdirectory will be searched and any HTML component that is found will be included 
    with an ID attribute with a unique value. This default value is a UUID code, but can be configured for another 
    form of generation. In addition there are other configuration parameters that can be used.

    Parameters:
        extensions: defines the extension that will be used to find the files for add the ID.
        exclude_tags: defines which tags the ID attribute will not be added.
        include_tags: defines which tags the ID attribute will be added. The default is to include all tags.
        recursive: sets whether the search for the files will be recursive or not.
        encoding: sets the file encoding.
        path: sets the base directory to find the files.
        prefix: define the id's prefix.
        sufix: define the id's sufix.

    Examples:
        AddRandomIdCommand().execute()
        AddRandomIdCommand(path="/tmp/).execute()
        AddRandomIdCommand(path="/tmp/, recursive=True).execute()
        AddRandomIdCommand(path="/tmp/, recursive=True, exclude_tags=[html, head]).execute()
        
    Dependencies:
        BeautifulSoup
        uuid
        
    @author Clayton Boneli.
    """

    # Defines the extension of the files that will be used to add the ID attribute
    __EXTENSIONS = ["html", "hml", "xhtml"]

    # Defines which tags the ID attribute will not be added
    __EXCLUDE_TAGS = ['script', 'head', 'title', 'html', 'br', 'style']

    # Defines which tags the ID attribute will be added
    __INCLUDE_TAGS = ['*']

    # Sets whether the search for the files will be recursive or not
    __RECURSIVE = False

    # Sets the file encoding
    __ENCODING = "utf-8"

    # Sets the base directory to find the files
    __PATH = "."

    # Define the id's prefix
    __PREFIX = ""

    # Define the id's suffix
    __SUFFIX = ""

    def __init__(self, *args, **kwargs):
        self.path = self._get_path(**kwargs)
        self.recursive = self._get_recursive(**kwargs)
        self.exclude_tags = self._get_exclude_tags(**kwargs)
        self.include_tags = self._get_include_tags(**kwargs)
        self.encoding = self._get_encoding(**kwargs)
        self.extensions = self._get_extensions(**kwargs)
        self.prefix = self._get_prefix(**kwargs)
        self.suffix = self._get_suffix(**kwargs)

    def execute(self):
        file_names = self._find_file_names()
        for filename in file_names:
            document = self._read(filename)
            document_with_id = self._include_id(document)
            self._save(filename, document_with_id)

    def _get_suffix(self, **kwargs):
        return kwargs.get('suffix', self.__SUFFIX)

    def _get_prefix(self, **kwargs):
        return kwargs.get('prefix', self.__PREFIX)

    def _get_encoding(self, **kwargs):
        return kwargs.get('encoding', self.__ENCODING)

    def _get_extensions(self, **kwargs):
        return kwargs.get('extensions', self.__EXTENSIONS)

    def _get_recursive(self, **kwargs):
        return kwargs.get('recursive', self.__RECURSIVE)

    def _get_path(self, **kwargs):
        return kwargs.get('path', self.__PATH)

    def _get_exclude_tags(self, **kwargs):
        return kwargs.get('exclude_tags', self.__EXCLUDE_TAGS)

    def _get_include_tags(self, **kwargs):
        return kwargs.get('include_tags', self.__INCLUDE_TAGS)

    def _save(self, filename, document):
        with open(filename, encoding=self.encoding, mode="w") as file:
            file.write(document)

    def _include_id(self, document):
        soup = BeautifulSoup(document, 'html.parser')
        for tag in soup.descendants:
            if not self._is_valid_tag(tag) or tag.get('id'):
                continue
            tag['id'] = self._new_id(document, soup, tag)
        return str(soup)

    def _is_valid_tag(self, tag):
        return isinstance(tag, Tag) and tag.name.lower() not in self.exclude_tags and (
                self.include_tags == self.__INCLUDE_TAGS or tag.name.lower() in self.include_tags
        )

    def _new_id(self, document, soup, tag):
        return self.prefix + str(uuid.uuid4()) + self.suffix

    def _read(self, filename):
        with open(filename, encoding=self.encoding, mode="r") as file:
            lines = file.readlines()
            return "".join(lines)

    def _is_valid_extension(self, filename):
        for ext in self.extensions:
            extension = ("." if "." not in ext else "") + ext.lower()
            if filename.lower().endswith(extension):
                return True
        return False

    def _find_file_names(self):
        result = []
        for root, directories, files in os.walk(self.path):
            if not self.recursive:
                directories.clear()

            for file in files:
                filename = os.path.join(root, file)
                if self._is_valid_extension(filename):
                    result.append(filename)

        return result
