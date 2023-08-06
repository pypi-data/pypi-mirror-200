import os
import sys
import traceback
import asyncio
from typing import Optional, Any, Callable

from quart import Quart, session, g, url_for, redirect
from quart.debug import traceback_response
from quart.typing import ASGILifespanProtocol, LifespanScope
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperConfig

from quart_keycloak import Keycloak


class ASGILifespanKroket(ASGILifespanProtocol):
    """Makes Quart lifespan.startup exceptions actually readable. Use only in development."""
    def __init__(self, app: Quart, scope: LifespanScope) -> None:
        self.app = app
        super().__init__(app, scope)

    async def __call__(self, receive: Callable, send: Callable) -> None:
        while True:
            event = await receive()
            if event["type"] == "lifespan.startup":
                try:
                    await self.app.startup()
                except Exception as error:
                    traceback.print_exc(file=sys.stderr)
                    os._exit(1)
                else:
                    await send({"type": "lifespan.startup.complete"})
            elif event["type"] == "lifespan.shutdown":
                try:
                    await self.app.shutdown()
                except Exception as error:
                    await send({"type": "lifespan.shutdown.failed", "message": str(error)})
                else:
                    await send({"type": "lifespan.shutdown.complete"})
                break


class QuartKroket(Quart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jinja_env.trim_blocks = True
        self.jinja_env.lstrip_blocks = True

        self.keycloak: Optional[Keycloak] = None

        from quart_kroket.template_filters import func_map
        for k, _func in func_map.items():
            self.add_template_filter(_func)

        @self.errorhandler(500)
        @self.errorhandler(400)
        async def page_error(e):
            from quart import render_template
            msg = f"Error occurred: {e.description}"
            self.logger.error(msg)
            return await render_template('errors/500.html', code=e.code), 500

        @self.errorhandler(403)
        async def page_forbidden(e):
            from quart import render_template
            return await render_template('errors/403.html', code=403, msg="Forbidden"), 403

        @self.errorhandler(404)
        async def page_not_found(e):
            from quart import render_template
            return await render_template('errors/404.html', code=404, msg="Page not found"), 404

        @self.before_request
        async def before_request():
            from quart_keycloak import KeycloakAuthToken
            from dacite import from_dict

            g.user = None
            g.ses = None
            auth_token = session.get("oidc_auth_token")
            if auth_token:
                auth_token_obj: KeycloakAuthToken = from_dict(
                    data_class=KeycloakAuthToken,
                    data=auth_token)
                g.ses = auth_token_obj

    async def setup_image_apis(self):
        """QR, avatar, gravatar APIs"""
        from quart_kroket.imaging.routes import route_imaging_gravatar, route_imaging_qr, route_imaging_avatar
        self.add_url_rule("/_/avatar/<path:inp>", "kquart.route_avatar", view_func=route_imaging_avatar)
        self.add_url_rule("/_/gravatar/<path:inp>", "kquart.route_gravatar", view_func=route_imaging_gravatar)
        self.add_url_rule("/_/qr/<path:inp>", "kquart.route_qr", view_func=route_imaging_qr)
        self.add_url_rule("/_/qr/<path:inp>/<path:color_from>/<path:color_to>/", "kquart.route_qr", view_func=route_imaging_qr)

    def setup_cache(self, session_protection: bool = False):
        from quart_session import Session
        self.config['SESSION_TYPE'] = 'redis'
        self.config['SESSION_PROTECTION'] = session_protection
        Session(self)

    def setup_keycloak(self, client_id: str, client_secret: str, configuration: str):
        from quart_keycloak import Keycloak
        self.keycloak = Keycloak(self, **{
            "client_id": client_id,
            "client_secret": client_secret,
            "configuration": configuration
        })

        @self.route('/oidc/login')
        async def oidc_login():
            login_url_keycloak = url_for(self.keycloak.endpoint_name_login)
            return redirect(login_url_keycloak)

        @self.route("/oidc/logout")
        async def oidc_logout():
            logout_url_keycloak = url_for(
                self.keycloak.endpoint_name_logout,
                redirect_uri=url_for('oidc_after_logout', _external=True))
            return redirect(logout_url_keycloak)

        @self.route("/oidc/after_logout")
        async def oidc_after_logout():
            session.clear()
            return redirect(url_for('bp_routes.root'))

    def run(
            self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            debug: Optional[bool] = None,
            use_reloader: bool = True,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            ca_certs: Optional[str] = None,
            certfile: Optional[str] = None,
            keyfile: Optional[str] = None,
            **kwargs: Any,
    ):
        from hypercorn.config import Config

        config = Config()
        config.bind = [f"{host}:{port}"]
        config.graceful_timeout = 0  # immediately quit hypercorn
        config.use_reloader = use_reloader
        config.ca_certs = ca_certs
        config.certfile = certfile
        config.keyfile = keyfile

        # setting `debug` has no effect, instead:
        # 1. activate the loop in debug mode
        # 2. `app.debug = True`

        for k, v in kwargs.items():
            setattr(config, k, v)

        if kwargs.get('debug', False):
            self.logger.info(f"Installing 'ASGILifespanKroket' because app.run(debug=True)")
            self.asgi_lifespan_class = ASGILifespanKroket
        asyncio.run(serve(self, config))
