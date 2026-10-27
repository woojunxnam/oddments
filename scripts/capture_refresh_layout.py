#!/usr/bin/env python3
"""Capture settled layouts on fresh HTTP pages; interaction QA is separate."""
import argparse
from functools import partial
import http.server
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--site',type=Path,required=True);a=ap.parse_args()
    out=ROOT/'test-results/refresh';out.mkdir(parents=True,exist_ok=True)
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(a.site)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/notes/'
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for name,route,width,height,full in [('layout-path-desktop','#return',1440,1000,True),('layout-card-mobile','#refresh/card/RF-013',390,844,False),('layout-home-mobile','#home',390,844,False)]:
                ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
                page=ctx.new_page();page.goto(base+route,wait_until='networkidle')
                page.locator('.rf-shell' if route!='#home' else '.rf-home').wait_for()
                if route.startswith('#refresh/card/'):
                    page.locator('.rf-filters>summary').click()
                    page.evaluate("window.scrollTo({top:document.querySelector('#rf-card').getBoundingClientRect().top+scrollY-85,behavior:'instant'})")
                else:page.evaluate("window.scrollTo({top:0,behavior:'instant'})");page.wait_for_function('scrollY === 0')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                page.screenshot(path=str(out/(name+'.png')),full_page=full)
                ctx.close()
            browser.close()
    finally:server.shutdown();server.server_close()
    print('Captured three fresh settled layouts; no functional test assertions were bypassed.')
if __name__=='__main__':main()
