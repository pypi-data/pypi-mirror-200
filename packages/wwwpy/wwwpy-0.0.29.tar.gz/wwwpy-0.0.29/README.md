Wwwpy helps you share Python code between server and browser.
It lives on top of [Pyodide](https://github.com/pyodide/pyodide).


# What's the benefit
Use Python all the way down, Python executing in the browser and (as usual) on the server.

This reduces costs and time of development. 
It avoids the impedance of having two different languages (e.g, Javascript in the browser and Python on the server).

# How it works

Thanks to Pyodide, it's possible to install and run Python packages in the browser.

Wwwpy is an opinionated microframework that helps to be productive quickly.
What Wwwpy can do for you:
- Start Pyodide
- Bring Python files in the browser
- Manage browser side Python dependencies
- Lower the cost of browser/server communications
- Provide Python helpers to deal with html/dom/javascript

## 1) Start Pyodide
We just read and implemented the Pyodide documentation.

## 2) Bring Python files in the browser
We build a zip with the sources we want in the browser and send it.
Thus, we need a web server and a handler.
 
## 3) Manage browser side Python dependencies
Load packages in the browser (Pyodide related). 
Again we use Pyodide 

## 4) Lower the cost of browser/server communications
RPC mechanism

## 5) Provide Python helpers to deal with html/dom/javascript
Widget(s) and HTML stubs

# Wwwpy lifecycle

- Configure a web server to serve 
  - client_bundle.zip, this contains the Python sources we want to send to the client
  - index.html, optional you can inject your html
  - pynanto_starter.js
  - rpc handlers
- 

# Impedance breaker projects
These are other projects that allow the developer to use the same language also in the browser. 
We can think of the following:
- NodeJs/Javascript (Javascript)
- Kotlin Multiplatform jvm/js (Kotlin)
- Clojure/Clojurescript (Clojure)
- Blazor WebAssembly (C#)



### Development Setup

1. `conda-create - 3.7`
1. `python -m pip install -e .[test]`
1. `python -m pip install -e .[dev]`
1. `python -m pip install -e .[testenv]`

