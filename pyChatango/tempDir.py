import os
import tempfile


def temp_dir(base_name="playwrigth_temp_dir"):
    temp_dir = tempfile.gettempdir()
    app_temp_dir = os.path.join(temp_dir, base_name)
    if not os.path.exists(app_temp_dir):
        os.makedirs(app_temp_dir)

    return app_temp_dir
