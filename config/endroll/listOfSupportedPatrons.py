
from ..patrons_list import PATRONS_LIST
from ..._version import ADDON_NAME, CUSTOM_OR_CREATED



def clink(name, text,url=None):
    if not url:
        return f'{name} : {text}<br>'
    return f'{name} : <a href="{url}" target="_blank">{text}</a><br>'

credits = """
<br><br><br>
<b>[ CREDIT ]</b>
<br><br><br>
""".replace('\n', '<br>')

patrons_list = PATRONS_LIST.replace(",", "<br>")


patreon = """
Special Thanks
<b>[ PATRONS ]</b>
{patrons_list}
""".format(patrons_list=patrons_list).replace('\n', '<br>')

sound =("<b>[ SOUNDS & BGM ]</b><br>"+
clink ("", "" , "")+
""
)


caractor = ("<b>[ IMAGE&3D MATERIALS ]</b><br>" +
clink ("", "" , "")+
""
            )


addons = ("<b>[ Images ]</b><br>"+
clink ("", "" , "")+

""
)

# """.replace('\n', '<br>')

budle = ("<b>[ Credit ]</b><br>" +
clink ("", "" , "")+

""
)


thankYou = ("""
<br><br><br>
<h3>%s</h3><br>""" % ADDON_NAME +
clink(f"{CUSTOM_OR_CREATED} by", "Shigeyuki","https://www.patreon.com/Shigeyuki")+
"""
<br>
Thank you very much!
<br><br><br><br>
""")