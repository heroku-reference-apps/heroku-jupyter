class HelloWorldHandler(IPythonHandler):
        def get(self):
            self.finish('Hello, world!')

try:
    import os
    import json
    import traceback
    import pgcontents
    from notebook.auth import passwd
    from notebook.utils import url_path_join
    from notebook.base.handlers import IPythonHandler
    
  

    def load_jupyter_server_extension(nb_server_app):
        web_app = nb_server_app.web_app
        host_pattern = '.*$'
        route_pattern = url_path_join(web_app.settings['base_url'], '/hello')
        web_app.add_handlers(host_pattern, [(route_pattern, HelloWorldHandler)])

    c = get_config()
    
    ### Password protection ###
    # http://jupyter-notebook.readthedocs.io/en/latest/security.html
    if os.environ.get('JUPYTER_NOTEBOOK_PASSWORD_DISABLED') != 'DangerZone!':
        password = os.environ['JUPYTER_NOTEBOOK_PASSWORD']
        c.NotebookApp.password = passwd(password)
        load_jupyter_server_extension()
    else:
        c.NotebookApp.token = ''
        c.NotebookApp.password = ''

    ### PostresContentsManager ###
    database_url = os.getenv('DATABASE_URL', None)
    if database_url:
        # Tell IPython to use PostgresContentsManager for all storage.
        c.NotebookApp.contents_manager_class = pgcontents.PostgresContentsManager

        # Set the url for the database used to store files.  See
        # http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#postgresql
        # for more info on db url formatting.
        c.PostgresContentsManager.db_url = database_url

        # PGContents associates each running notebook server with a user, allowing
        # multiple users to connect to the same database without trampling each other's
        # notebooks. By default, we use the result of result of getpass.getuser(), but
        # a username can be specified manually like so:
        c.PostgresContentsManager.user_id = 'heroku'

        # Set a maximum file size, if desired.
        #c.PostgresContentsManager.max_file_size_bytes = 1000000 # 1MB File cap

    ### CloudFoundry specific settings
    vcap_application_json = os.getenv('VCAP_APPLICATION', None)
    if vcap_application_json:
        vcap_application = json.loads(vcap_application_json)
        uri = vcap_application['uris'][0]
        c.NotebookApp.allow_origin = 'https://{}'.format(uri)
        c.NotebookApp.websocket_url = 'wss://{}:4443'.format(uri)

except Exception:
    traceback.print_exc()
    # if an exception occues, notebook normally would get started
    # without password set. For security reasons, execution is stopped.
    exit(-1)
