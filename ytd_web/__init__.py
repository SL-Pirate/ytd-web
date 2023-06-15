from flask import Blueprint

from ytd_web.home import home_page
from ytd_web.search import search_page
from ytd_web.browse import browse_page
from ytd_web.select import select_page
from ytd_web.multimedia import multimedia_page
from ytd_web.get_mulimedia import get_miltimedia_page
from ytd_web.download import download_page
from ytd_web.error import error_page
from ytd_web.login_signup import login_signup_page
from ytd_web.dashboard import dashboard_page

endpoints: list[Blueprint] = [
    home_page, 
    search_page, 
    browse_page, 
    select_page, 
    multimedia_page, 
    get_miltimedia_page, 
    download_page, 
    error_page,
    login_signup_page,
    dashboard_page
]
