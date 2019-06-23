#%%

from markdown import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

mdstr1 = '# Heading 1\n## Heading 2\n### Heading 3\n'
mdstr2 = r'$$\sigma = \frac{\tau}{2}$$'

print(markdown(mdstr1+mdstr2, extensions=[GithubFlavoredMarkdownExtension()]))

# display_markdown(md)

# print(html)

