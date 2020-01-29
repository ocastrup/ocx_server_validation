[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Welcome

The server side OCX validator is built on Flask and the **flaskboilerplate** from the skeleton app:  
[http://www.flaskboilerplate.com/](http://www.flaskboilerplate.com/).
The **Flask** app is dockerized and can readily be deployed on Docker [https://www.docker.com/](https://www.docker.com/). 
The container is stateless.
### Build
docker build -t ocx-validate .
### run
docker run -p 5000:5000 --name ocx-validate -d ocx-validate:latest 
<hr>

**What is Flask?** Flask is a microframework for Python based on Werkzeug and Jinja2.

Project Structure
--------

  ```sh
  ├── README.md
  ├── app.py
  ├── config.py
  ├── error.log
  ├── forms.py
  ├── Dockerfile
  ├── requirements.txt
  ├── static
  │   ├── css
  │   │   ├── bootstrap-3.0.0.min.css
  │   │   ├── bootstrap-theme-3.0.0.css
  │   │   ├── bootstrap-theme-3.0.0.min.css
  │   │   ├── font-awesome-3.2.1.min.css
  │   │   ├── layout.forms.css
  │   │   ├── layout.main.css
  │   │   ├── main.css
  │   │   ├── main.quickfix.css
  │   │   └── main.responsive.css
  │   ├── fonts
  │   │   ├── FontAwesome.otf
  │   │   ├── fontawesome-webfont.eot
  │   │   ├── fontawesome-webfont.svg
  │   │   ├── fontawesome-webfont.ttf
  │   │   └── fontawesome-webfont.woff
  │   ├── ico
  │   │   ├── approved-touch-icon-114-precomposed.png
  │   │   ├── approved-touch-icon-144-precomposed.png
  │   │   ├── approved-touch-icon-57-precomposed.png
  │   │   ├── approved-touch-icon-72-precomposed.png
  │   │   └── favicon.png
  │   ├── img
  │   └── js
  │       ├── libs
  │       │   ├── bootstrap-3.0.0.min.js
  │       │   ├── jquery-1.10.2.min.js
  │       │   ├── modernizr-2.6.2.min.js
  │       │   └── respond-1.3.0.min.js
  │       ├── plugins.js
  │       └── script.js
  └── templates
  |   ├── errors
  |   │   ├── 404.html
  |   │   └── 500.html
  |   |   └── syntax_error.html
  |   ├── forms
  |   │   ├── report.html
  |   │   ├── select.html
  |   │   └── validate.html
  |   ├── layouts
  |   │   ├── form.html
  |   │   └── main.html
  |   └── pages
  |       ├── placeholder.about.html
  |       └── placeholder.home.html
  └── Python app specific modules
  └── ```
