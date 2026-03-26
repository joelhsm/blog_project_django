import os
import re
from html.parser import HTMLParser

class TagChecker(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.stack = []
        self.void_elements = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def handle_starttag(self, tag, attrs):
        if tag not in self.void_elements:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.void_elements:
            return
        if not self.stack:
            print(f"{self.filename}:{self.getpos()[0]}: Unexpected end tag </{tag}>")
            return
        # Find the matching start tag
        found = False
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                found = True
                # Report unclosed tags inside
                for unclosed_tag, pos in self.stack[i+1:]:
                    print(f"{self.filename}:{pos[0]}: Unclosed start tag <{unclosed_tag}> before </{tag}>")
                self.stack = self.stack[:i]
                break
        if not found:
            print(f"{self.filename}:{self.getpos()[0]}: Unexpected end tag </{tag}> (no matching start)")

    def check_remaining(self):
        for tag, pos in self.stack:
            if tag not in ('!doctype', 'html', 'body', 'head'):  # simple exceptions that html parser sometimes misses or are optional
                print(f"{self.filename}:{pos[0]}: Unclosed HTML start tag <{tag}> at end of file")

def check_django_tags(content, filename):
    stack = []
    pairs = {
        'if': 'endif',
        'for': 'endfor',
        'block': 'endblock',
        'with': 'endwith',
        'ifequal': 'endifequal',
        'filter': 'endfilter'
    }
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        line_num = i + 1
        tags = re.findall(r'{%\s*(\w+)[^%]*%}', line)
        for tag in tags:
            if tag in pairs:
                stack.append((tag, line_num))
            elif tag in pairs.values():
                if not stack:
                    print(f"{filename}:{line_num}: Unexpected Django end tag {{% {tag} %}}")
                    continue
                expected_start = [k for k, v in pairs.items() if v == tag][0]
                found = False
                for j in range(len(stack) - 1, -1, -1):
                    if stack[j][0] == expected_start:
                        found = True
                        for unclosed_tag, pos in stack[j+1:]:
                            print(f"{filename}:{pos}: Unclosed Django start tag {{% {unclosed_tag} %}} before {{% {tag} %}}")
                        stack = stack[:j]
                        break
                if found:
                    pass
                else:
                    print(f"{filename}:{line_num}: Unexpected Django end tag {{% {tag} %}} (no matching start)")

    for tag, pos in stack:
        print(f"{filename}:{pos}: Unclosed Django start tag {{% {tag} %}} at end of file")

def main():
    templates_dir = '/home/joel-mafra/Documentos/udemy/blog_project/djangoapp/blog/templates'
    print("Checking templates...")
    for root, dirs, files in os.walk(templates_dir):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Check Django
                check_django_tags(content, path)
                
                # Check HTML (strip django tags)
                html_content = re.sub(r'{%.*?%}', '', content)
                html_content = re.sub(r'{{.*?}}', '', html_content)
                html_content = re.sub(r'{#.*?#}', '', html_content)
                parser = TagChecker(path)
                try:
                    parser.feed(html_content)
                    parser.check_remaining()
                except Exception as e:
                    pass

    print("Check complete.")

if __name__ == '__main__':
    main()
