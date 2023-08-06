import os
from urllib.parse import urlsplit


class ParsedQueryString:
    """
    Encapsulates the parsing and setting of query string parameters
    """
    def __init__(self, query_string):
        self.original_qs = query_string
        self.qs = query_string.strip()
        # strip off the ? if still there
        if self.qs.startswith("?"):
            self.qs = self.qs[1:]
        # split each param based on & (should be x=xval, y=yval etc)
        exp_params = self.qs.split("&")
        self.params = {}
        for exp_param in exp_params:
            items = exp_param.split("=")
            if len(items) >= 2:
                self.params[items[0]] = items[1]

    def __str__(self):
        """
        By default, the query string will be the params dict put back together without the ?
        :return:
        """
        qs = ""
        for key, value in self.params.items():
            qs += key + "=" + str(value) + "&"
        if qs:
            qs = qs[:-1]
        return qs


class ParsedUrl:
    """
        Encapsulates the parsing and setting up url values so we don't have this code everywhere being done differently.
        Basic idea is to pass a string url (possibly relative) and a default_scheme and netloc to create absolute urls.
        Then allow developers to get or adjust the values they need.

        Ex: {url=test.html, default_netloc=//www.ex.org} -> //www.ex.org/test.html
        Ex: {url=https://www.site2.com/something/, default_netloc=//www.ex.org} -> https://site2.com/something/
        Ex: {url=test.html, default_netloc=None} -> test.html

        We want a way to ask for a relative or fully qualified url including fragments and querystings or not
    """
    def __init__(self, url: str, default_netloc: str = None, default_scheme: str = None, allow_fragments: bool = True):
        self.original_url = url
        if self.url_filter(url) is None or len(self.url_filter(url)) == 0:
            raise Exception(
                f'Attempted to parse [{str(self.url_filter(url))}].  Url parameter must exist and be a relative or absolute url after filtering!')
        self.parsed = urlsplit(self.url_filter(url), default_scheme or "", allow_fragments=allow_fragments)
        if default_netloc and not self.parsed.netloc:
            self.netloc = default_netloc
        if default_scheme and not self.parsed.scheme and self.netloc:
            self.scheme = default_scheme
        # one last correction; if we have a scheme but no netloc lets omit the scheme so it doesn't give bad results
        if not self.parsed.netloc and self.parsed.scheme:
            self.parsed = self.parsed._replace(scheme='')

    @property
    def filepath(self):
        return os.path.dirname(self.parsed.path)

    @property
    def filename(self):
        return os.path.basename(self.parsed.path)

    @property
    def fileext(self):
        return os.path.splitext(self.filename)[1]

    @property
    def url(self):
        # NOTE: since we are joining and applying filters in the constructor we just return the value here
        #   no setter needed to force constructor only
        return self.parsed.geturl()

    @property
    def base(self):
        # NOTE: url_base is always the current parsed minus any qs or fragment values
        return self.parsed._replace(query='', fragment='').geturl()

    @property
    def rel(self):
        # NOTE: url_rel is the current parsed minus any scheme or domain
        return self.parsed._replace(netloc='', scheme='').geturl()

    @property
    def port(self):
        # NOTE: port is set by netloc but readable separately
        return self.parsed.port

    @property
    def qs(self):
         return self.parsed.query

    @qs.setter
    def qs(self, value):
        self.parsed = self.parsed._replace(query=value)

    @property
    def fragment(self):
        return self.parsed.fragment

    @fragment.setter
    def fragment(self, value):
        self.parsed = self.parsed._replace(fragment=value)

    # adding the netloc back in since domain = hostname
    @property
    def netloc(self):
        return self.parsed.netloc

    @netloc.setter
    def netloc(self, value):
        self.parsed = self.parsed._replace(netloc=value)

    @property
    def domain(self):
        return self.parsed.hostname

    @domain.setter
    def domain(self, value):
        if self.parsed.port and str(self.parsed.port) not in value:
            value += f":{self.parsed.port}"
        self.parsed = self.parsed._replace(netloc=value)

    @property
    def scheme(self):
        return self.parsed.scheme

    @scheme.setter
    def scheme(self, value):
        self.parsed = self.parsed._replace(scheme=value)

    @property
    def path(self):
        return self.parsed.path

    @path.setter
    def path(self, value):
        self.parsed = self.parsed._replace(path=value)

    @property
    def root_domain(self):
        domain = self.domain
        if domain:
            pos = domain.rfind(".")
            if pos > -1:
                pos = domain.rfind(".", 0, pos)
                if pos > -1:
                    return domain[pos + 1:]
        return domain

    def get_param(self, key):
        pqs = ParsedQueryString(self.qs)
        return pqs.params.get(key, None)

    def set_param(self, key, value):
        # first load our existing params so we replace if it exists
        pqs = ParsedQueryString(self.qs)
        pqs.params[key] = value
        self.parsed = self.parsed._replace(query=str(pqs))

    def del_param(self, key):
        # first load our existing params so we replace if it exists
        pqs = ParsedQueryString(self.qs)
        if key in pqs.params:
            pqs.params.pop(key)
        self.parsed = self.parsed._replace(query=str(pqs))

    @staticmethod
    def url_filter(url):
        """
        Allows for modifying the url parameter before any parsing
        :return: modified url
        """
        # by default, we will simply strip any leading/trailing whitespace
        if url:
            return url.strip()
        return url

    def __str__(self):
        """
        By default, the string value is the fully qualified url (as much as we have)
        :return:
        """
        return self.url


if __name__ == "__main__":
    # test_uri = "http://localhost:8000/test1/?id=1&x=2"
    # parsed_url = ParsedUrl(test_uri)
    # print(f"root domain [{test_uri}]: {parsed_url.get_root_domain()}")
    # print(f"url:{parsed_url.url}")
    test_uri = "/?id=1&b=&c=3"
    parsed_url = ParsedUrl(test_uri, default_netloc='ex.org')
    print(f"root domain [{test_uri}]: {parsed_url.root_domain}")
    print(f"url:{parsed_url.url}")
    print(f"base: {parsed_url.base}")
    print(f"rel: {parsed_url.rel}")
    print(f"url after base: {parsed_url.url}")
    parsed_url.domain = "ex.org"
    print(f"root domain [{str(parsed_url)}]: {parsed_url.root_domain}")
    test_uri = "ex.org/"
    print(f"root domain [{test_uri}]: {ParsedUrl(test_uri).root_domain}")
    test_uri = "http://www.ex.org/go/"
    print(f"root domain [{test_uri}]: {ParsedUrl(test_uri).root_domain}")
    test_uri = "http://store.ex.org/go/"
    print(f"root domain [{test_uri}]: {ParsedUrl(test_uri).root_domain}")
