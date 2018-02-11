import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
# language choice depends on LANGUAGE environment variable
translate = gettext.translation('fiasko_bro', localedir, fallback=True)
_ = translate.gettext
