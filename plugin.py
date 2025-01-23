import re
import os
import json
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.pages import Page
from pymdownx.slugs import slugify

logger = get_plugin_logger(__name__)
header_slugify = slugify(case = "lower-ascii")
header_pattern : re.Pattern = re.compile(r'(^#{1,6}\s+.*?)(?:\s*\{\s*helpId\s*:\s*(\d+)\s*\})+\s*$', re.IGNORECASE | re.MULTILINE)

global_dict = {}

def on_pre_build(config):
    global_dict.clear()

def on_post_build(config):
    output_dir = config['site_dir']

    html_content = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Redirecting...</title>
    <script>
       (function (){{
          var regex = new RegExp('[#&]cshid=([^&#]*)');
          var results = regex.exec(window.location.href);
          var cshid = null;
          if(results !== null){{
            cshid = results[1];
          }}

          var rootUrl = 'default.htm';
          var baseUrl = window.location.pathname.replace(rootUrl, "");

          var redirects = {global_dict}
      
        var redirectUrl = redirects[cshid] || "index.html";

        window.location.replace(baseUrl + redirectUrl);
      }})();
    </script>

</head>

<body>
    <p>Redirecting...</p>
</body>

</html>
"""
    with open(os.path.join(output_dir, 'default.htm'), 'w') as f:
        f.write(html_content)

def on_page_markdown(markdown: str, page: Page, config, files):

    # Look for a page level helpId in the page meta data.
    value = find_meta_entry(page.meta, "helpId")
    if value:
        add_global_link(value, page.url)

    # Callback for regex sub function.
    def sub_cb(match):
        text, id = match.groups()

        # Slugify the header name, this *should* be the same as the generate id.
        # There is a chance its not the same, check if links aren't working.
        linkpoint = page.url + "#" + header_slugify(text,"-").lstrip('-')

        # Try to add this to the global link mapping.
        add_global_link(id, linkpoint)

        # Return the text without the help Id block. 
        return text

    return re.sub(header_pattern, sub_cb, markdown)

def find_meta_entry(map, keyName):
    for key in map:
        if(key.lower() == keyName.lower()):
            return map[key];
    return None

def add_global_link(id: str, link:str):
    if not isinstance(id, int) and not id.isdigit():
        logger.warning(f"Help Id is not of type int: '{id}'")
        return
    nid = int(id)
    if nid in global_dict:
        duplicate_entry = global_dict[nid]
        logger.warning(f"Duplicate Help Id Entries for {nid}:\r\n\t{duplicate_entry}\r\n\t{link} ")
    global_dict[nid] = link
