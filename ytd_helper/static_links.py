from flask import url_for
from ytd_helper.error import NotInstanciatedError

class StaticLinks:
    _context = None
    _isInstanciated = False

    _home = "home_page.home"
    _search = "search_page.search"
    _browse = "browse_page.browse"
    _select = "select_page.select"
    
    _download_end = "download_page"
    _export = _download_end + ".export"
    _export_aud = _download_end + ".export_aud"

    _multimedia_end = "multimedia_page"
    _download_vid = _multimedia_end + ".download_vid"
    _download_aud = _multimedia_end + ".download_aud"
    _error = "error_page.error"
    
    _file_get = ".file_get"

    _get_multimedia_via_api_end = "get_multimedia_via_api"
    _file_get_aud = _get_multimedia_via_api_end + ".file_get_aud"
    _download_from_link = _get_multimedia_via_api_end + ".download_from_link"

    def __init__(self, context) -> None:
        StaticLinks._context = context
        StaticLinks._isInstanciated = True

    @staticmethod
    def isInstanciated() -> bool:
        return StaticLinks._isInstanciated

    @staticmethod
    def validate():
        if not StaticLinks.isInstanciated():
            raise NotInstanciatedError

    @staticmethod
    def getUrlFor(end: str):
        '''
            creates an endpoint for pages with no request args
        '''
        StaticLinks.validate()
        with StaticLinks._context:
            return url_for(end)

# _____________________________ links __________________________________
    @staticmethod
    def select(yt_link: str):
        StaticLinks.validate()
        with StaticLinks._context:
            return url_for(StaticLinks._select, link=yt_link)
        
    @staticmethod
    def browse(yt_link: str):
        StaticLinks.validate()
        with StaticLinks._context:
            return url_for(StaticLinks._browse, q=yt_link)
    
    @staticmethod
    def export_aud():
        return StaticLinks.getUrlFor(StaticLinks._export_aud)
    
    @staticmethod
    def export():
        return StaticLinks.getUrlFor(StaticLinks._export)
    
    @staticmethod
    def home():
        return StaticLinks.getUrlFor(StaticLinks._home)
    
    @staticmethod
    def download_vid(resolution):
        StaticLinks.validate()
        with StaticLinks._context:
            return url_for(StaticLinks._download_vid, reso=resolution)
        
    @staticmethod
    def download_aud(quality):
        StaticLinks.validate()
        with StaticLinks._context:
            return url_for(StaticLinks._download_aud, qual=quality)
        
    @staticmethod
    def error():
        return StaticLinks.getUrlFor(StaticLinks._error)
    
    @staticmethod
    def search(yt_link):
        StaticLinks.validate()
        with StaticLinks._context:
            return url_for(StaticLinks._search, link=yt_link)
        
    @staticmethod
    def file_get():
        return StaticLinks.getUrlFor(StaticLinks._file_get)
    
    @staticmethod
    def file_get_aud():
        return StaticLinks.getUrlFor(StaticLinks._file_get_aud)

    @staticmethod
    def download_from_link(_file):
        StaticLinks.validate()
        with StaticLinks._context:
            return url_for(StaticLinks._download_from_link, file_name=_file)