# heroku-jupyter

Use this application to deploy [Jupyter Notebook](https://jupyter.org/) to
Heroku. If a postgres database is available,
[pgcontents](https://github.com/quantopian/pgcontents) is used to power persistant notebook
storage.

If you want to customize your app, feel free to fork this repository.

## Quick start - Installation instructions

The fastest & easiest way to get started is to choose option 1 below: automatic deployment on Heroku.

### 1. Heroku - Automatic Deployment (faster & easier)

First, click on this handy dandy button:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Go through the form that the ^^ above button leads you to, and choose an app name, password, and whether to run Jupyter notebook or Jupyter lab. Then click the purple 'deploy app' button at the bottom of the form.

It will take a couple of minutes for your app to deploy, and then you'll be able to click links to 1) manage your app, and 2) view your live, interactive jupyter application running on a heroku dyno (with persistant storage!).

Note: If you choose later to fork this repository, you can link your new repo to your heroku app afterwards.

### 2. Heroku - Manual Deployment (does the same thing as 1, but nice for learning / understanding)

Push this repository to your app or fork this repository on github and link your
repository to your heroku app.

To create a new app, run:
```
export APP_NAME=<your_app_name>
export JUPYTER_NOTEBOOK_PASSWORD=<your_jupyter_password>
# set to 'notebook' or 'lab' to choose which jupyter application to launch:
export JUPYTER_NOTEBOOK_OR_LAB=<notebook_or_lab>

# if you don't have git:
brew install git
# clone this repo (swap with your forked repo if you wish):
git clone git@github.com:heroku/heroku-jupyter.git
cd heroku-jupyter

# Create a new app (or use an existing one you've made)
heroku create $APP_NAME

# Set the stack:
heroku stack:set heroku-24 --app $APP_NAME

# Set your required config variable:
heroku config:set JUPYTER_NOTEBOOK_PASSWORD=$JUPYTER_NOTEBOOK_PASSWORD -a $APP_NAME
heroku congif:set JUPYTER_NOTEBOOK_OR_LAB=$JUPYTER_NOTEBOOK_OR_LAB -a $APP_NAME

# Specify the buildpacks it should use:
heroku buildpacks:add --index 1 heroku-community/apt -a $APP_NAME
heroku buildpacks:add --index 2 heroku/python -a $APP_NAME

# Attach the postgres addon:
heroku addons:create heroku-postgresql:essential-1 --app $APP_NAME

# Connect your app to the repo:
heroku git:remote -a $APP_NAME

# deploy
git push heroku main

# Follow the URL from ^^ to view your app! To view logs, run `heroku logs --tail -a $APP_NAME`
```

Optional useful commands:
```
# show config variables:
heroku config --app $APP_NAME

# ssh into build
heroku run bash --app $APP_NAME

# view logs
heroku logs --tail -a $APP_NAME
```

If you are really sure that you do not want a password protected notebook and server (not recommended), you can set `JUPYTER_NOTEBOOK_PASSWORD_DISABLED` to `DangerZone!`:
```
heroku config:set JUPYTER_NOTEBOOK_PASSWORD_DISABLED=DangerZone! -a $APP_NAME
```

## Environment / Config variables
- `JUPYTER_NOTEBOOK_PASSWORD`: Set password for notebooks
- `JUPYTER_NOTEBOOK_PASSWORD_DISABLED`: Set to `DangerZone!` to disable password protection
- `JUPYTER_NOTEBOOK_ARGS`: Additional command line args passed to `jupyter notebook`; e.g. get a more verbose logging using `--debug`


## Python version

If you want to use a different Python version, you should set it in the `.python-version` file, for example:
```
3.11
```

