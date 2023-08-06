import os
from datetime import datetime

import jinja2

from quart import current_app
from quart_kroket.net.http_requests import post_json

_FONT_FAMILY = "Roboto Condensed, Helvetica, arial"
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


async def render_mjml_template(template_name, base_url: str, **kwargs) -> str:
    """
    Args:
        template_name: 'basic.jinja2'
        base_url: BASE URL to MJML API, e.g: https://foo.domain.bla/
        **kwargs:
    Returns:
    """
    if not template_name.endswith(".jinja2"):
        template_name += ".jinja2"

    loader = jinja2.FileSystemLoader(searchpath=os.path.join(_BASE_DIR, "templates"))
    env = jinja2.Environment(loader=loader)

    template = env.get_template(template_name)
    mjml = template.render(**kwargs)

    _url = f"{base_url}/mjml/4/html"
    current_app.logger.debug(f"translating mjml via URL {_url}")

    try:
        blob = await post_json(_url, {"mjml": mjml})
        return blob['html']
    except Exception as ex:
        raise Exception(f"Could not compile MJML->HTML; {ex}")


class MJMLText:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"""
<mj-text font-size="16px" font-family="{_FONT_FAMILY}">
    {self.text}
</mj-text>
        """
