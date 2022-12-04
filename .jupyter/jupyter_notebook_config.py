try:
    import os
    import json
    import traceback
    import pgcontents
    from notebook.auth import passwd
    from notebook.utils import url_path_join
    from notebook.base.handlers import IPythonHandler
    


    c = get_config()
    c.NotebookApp.ip = '0.0.0.0'


    ### Password protection ###
    # http://jupyter-notebook.readthedocs.io/en/latest/security.html
    if os.environ.get('JUPYTER_NOTEBOOK_PASSWORD_DISABLED') != 'DangerZone!':
        password = os.environ['JUPYTER_NOTEBOOK_PASSWORD']
        c.NotebookApp.password = passwd(password)
        
    else:
        c.NotebookApp.token = ''
        c.NotebookApp.password = ''

   

except Exception:
    traceback.print_exc()
    # if an exception occues, notebook normally would get started
    # without password set. For security reasons, execution is stopped.
    exit(-1)
