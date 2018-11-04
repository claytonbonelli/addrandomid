# AddRandomId

A Python library to dinamicaly include IDs into html tags.

Sometimes when we develop our HTML pages, we forget to include the unique identifiers (IDs) in our tags. 
Later we realize that when we need these identifiers, for example when we use automated testing tools, 
we must manually include those same IDs in each of the tags that will be tested, which is a tedious task. 
To avoid this manual work, this tool was developed with the mission of including unique identifiers (IDs) 
in all HTML tags that exist in the files.

The operation is very simple, you indicate the base directory where the HTML files can be found and recursively 
(configurable) each subdirectory will be searched and any HTML component that is found will be included 
with an ID attribute with a unique value. This default value is a UUID code, but can be configured for another 
form of generation. In addition there are other configuration parameters that can be used.

### Parameters:
   * extensions: defines the extension that will be used to find the files for add the ID.
   * exclude_tags: defines which tags the ID attribute will not be added.
   * include_tags: defines which tags the ID attribute will be added. The default is to include all tags.
   * recursive: sets whether the search for the files will be recursive or not.
   * encoding: sets the file encoding.
   * path: sets the base directory to find the files.
   * prefix: define the id's prefix.
   * sufix: define the id's sufix.

### Examples:

```python
    AddRandomIdCommand().execute()
    AddRandomIdCommand(path="/tmp/).execute()
    AddRandomIdCommand(path="/tmp/, recursive=True).execute()
    AddRandomIdCommand(path="/tmp/, recursive=True, exclude_tags=[html, head]).execute()
```

    
### Dependencies:
   * BeautifulSoup
   * uuid
    
