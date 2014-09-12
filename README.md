Docs!
====

Public documentation for TempoIQ.

Built docs are currently hosted on GitHub pages:http://tempoiq.github.io/docs/

To build docs locally:

1. `git clone <this repo>`
2. `cd docs/`
3. (optional) Switch into a Python virtualenv
4. `pip install -r requirements.txt`
5. `make html`

HTML output is in build/html.


## Conventions

### Headings

Use the following hierarchy for indicating headings in .rst:

h1:
```
============
Page heading
============
```

h2:
```
Section heading
---------------
```

h3:
```
Subsection heading
~~~~~~~~~~~~~~~~~~
```

h4 (but try to avoid hierarchies this deep):
```
Sub-subsection heading
^^^^^^^^^^^^^^^^^^^^^^
```
