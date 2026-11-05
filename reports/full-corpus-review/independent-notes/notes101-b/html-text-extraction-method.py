from html.parser import HTMLParser
from pathlib import Path
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.main=0;self.all=[];self.content=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
  if t=='main':self.main+=1
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
  if t=='main':self.main=max(0,self.main-1)
 def handle_data(self,d):
  if not self.skip and d.strip():
   self.all.append(d.strip())
   if self.main:self.content.append(d.strip())
for f in Path('reports/full-corpus-review/independent-notes/notes101-b/sources').glob('*.html'):
 p=P();p.feed(f.read_text(errors='replace'));f.with_suffix('.read.txt').write_text('\n'.join(p.content or p.all)+'\n')
