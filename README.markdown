Tracking hardware changes in python
===================================

This code is a simple flask app which prototypes the hardware changes using python.

Development
-----------

For development, the procfile lists the processes, one for running the web server and one for running the live reloader. To get set up perform the following steps:

1. (either in virtualenv or not) `pip install -r requirements.txt`
2. `bundle`
3. `foreman start`

This should give a live-reloading flask development server.

*Currently this project requires python2.7 and 2.7 only*
