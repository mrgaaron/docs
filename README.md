Docs!
====

Public documentation for TempoIQ.

Built docs are currently hosted on GitHub pages: http://tempoiq.github.io/docs/

To build docs locally:

1. `git clone <this repo>`
2. `cd docs/`
3. (optional) Switch into a Python virtualenv
4. `pip install -r requirements.txt`
5. `make html`

HTML output is in build/html. If you're feeling more adventurous, there's
also a Grunt task that auto-builds the docs and refreshes the webpage whenever
a .rst file changes. To set it up:

1. Install Node: e.g. `brew install node`
2. Install grunt: `npm install -g grunt-cli`
3. Install packages and grunt plugins to do the cool stuff: `npm install`
4. Run the task with `grunt`.


## Stuff to know

The "dev" Sphinx tag can be used to include content in development builds only,
e.g.:

    .. only:: dev

       Insert profanity, secrets, or other content that shouldn't be included
       in published docs.

The todo directive already has this behavior, so todos are never present in 
production docs.


## Organization

The FAQs page (/source/faqs.rst) can be used as a temporary holding area for
quickly answering questions that come up from customers. However, the page
should periodically be refactored, putting answers into more specific pages
to prevent it from sprawling out of control.


## Conventions

### Headings

Use the following hierarchy for indicating headings in .rst:

h1:

    ============
    Page heading
    ============


h2:

    Section heading
    ---------------


h3:

    Subsection heading
    ~~~~~~~~~~~~~~~~~~


h4 (but try to avoid hierarchies this deep):

    Sub-subsection heading
    ^^^^^^^^^^^^^^^^^^^^^^


### Terminology

* "data point" is two words
* "time zone" is two words
* "real time" or "real-time", not "realtime"
* "timestamp" is one word

### Punctuation/capitalization

* Use the oxford comma.
* File names should be in `kebab-case`
* Class names should be in `PascalCase` (except in filenames).
* To reflect the JSON API, multi-word field names should be in `snake_case`.
