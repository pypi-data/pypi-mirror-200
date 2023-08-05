from chatgpt_tool_hub.apps.app import App


def load_app(app_type: str = 'victorinox', tools_list: list = None, **tools_kwargs) -> App:

    if app_type == 'lite':
        from chatgpt_tool_hub.apps.lite_app import LiteApp
        app = LiteApp()
        app.create(tools_list, **tools_kwargs)
        return app

    elif app_type == 'victorinox':
        from chatgpt_tool_hub.apps.victorinox import Victorinox
        # default tool_list for Victorinox
        default_tools_list = ["python_repl", "requests", "terminal", "meteo-weather"]
        if not tools_list:
            tools_list = default_tools_list
        app = Victorinox()
        app.create(tools_list, **tools_kwargs)
        return app

    else:
        raise NotImplementedError
