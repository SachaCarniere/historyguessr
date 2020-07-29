import string
from html.parser import HTMLParser


class WikiThumbailExtractor(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._inbody = False
        self._ininfobox = False
        self._url = ""

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            _inbody = True
            print("in body")

        if tag == "div":
            for attr in attrs:
                if attr[0] == "class" and str(attr[0]).__contains__("infobox"):
                    self._ininfobox = True
                    print("in infobox")
                    return

        if self._ininfobox and tag == "img":
            for attr in attrs:
                if attr[0] == "src":
                    self._url = attr[1]
                    return

    def handle_endtag(self, tag):
        pass

    def get_img_src(self):
        return self._url



test = (
'''
<link rel="canonical" href="https://en.wikipedia.org/wiki/Thriller_(album)"/>
<link rel="dns-prefetch" href="//login.wikimedia.org"/>
<link rel="dns-prefetch" href="//meta.wikimedia.org" />
<!--[if lt IE 9]><script src="/w/resources/lib/html5shiv/html5shiv.js"></script><![endif]-->
</head>
<body class="mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject page-Thriller_album rootpage-Thriller_album skin-vector action-view skin-vector-legacy minerva--history-page-action-enabled">
<div id="mw-page-base" class="noprint"></div>
<div id="mw-head-base" class="noprint"></div>
<div id="content" class="mw-body" role="main">
	<a id="top"></a>
	<div id="siteNotice" class="mw-body-content"><!-- CentralNotice --></div>
	<div class="mw-indicators mw-body-content">
	<div id="mw-indicator-featured-star" class="mw-indicator"><a href="/wiki/Wikipedia:Featured_articles" title="This is a featured article. Click here for more information."><img alt="This is a featured article. Click here for more information." src="//upload.wikimedia.org/wikipedia/en/thumb/e/e7/Cscr-featured.svg/20px-Cscr-featured.svg.png" decoding="async" width="20" height="19" srcset="//upload.wikimedia.org/wikipedia/en/thumb/e/e7/Cscr-featured.svg/30px-Cscr-featured.svg.png 1.5x, //upload.wikimedia.org/wikipedia/en/thumb/e/e7/Cscr-featured.svg/40px-Cscr-featured.svg.png 2x" data-file-width="462" data-file-height="438" /></a></div>
	<div id="mw-indicator-pp-default" class="mw-indicator"><a href="/wiki/Wikipedia:Protection_policy#semi" title="This article is semi-protected."><img alt="Page semi-protected" src="//upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/20px-Semi-protection-shackle.svg.png" decoding="async" width="20" height="20" srcset="//upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/30px-Semi-protection-shackle.svg.png 1.5x, //upload.wikimedia.org/wikipedia/en/thumb/1/1b/Semi-protection-shackle.svg/40px-Semi-protection-shackle.svg.png 2x" data-file-width="512" data-file-height="512" /></a></div>
	</div>
	<h1 id="firstHeading" class="firstHeading" lang="en"><i>Thriller</i> (album)</h1>
	<div id="bodyContent" class="mw-body-content">
		<div id="siteSub" class="noprint">From Wikipedia, the free encyclopedia</div>
		<div id="contentSub"></div>
		<div id="contentSub2"></div>
		
		<div id="jump-to-nav"></div>
		<a class="mw-jump-link" href="#mw-head">Jump to navigation</a>
		<a class="mw-jump-link" href="#searchInput">Jump to search</a>
		<div id="mw-content-text" lang="en" dir="ltr" class="mw-content-ltr"><div class="mw-parser-output"><div role="note" class="hatnote navigation-not-searchable">For other albums titled Thriller, as well as other uses, see <a href="/wiki/Thriller_(disambiguation)#Music" class="mw-redirect mw-disambig" title="Thriller (disambiguation)">Thriller § Music</a>.</div>
<p class="mw-empty-elt">
</p>
'''
)

extractor = WikiThumbailExtractor()
extractor.feed(test)

print(extractor.get_img_src())


