# LibreOffice Developer Search

Simplified searching for LibreOffice Developers. This version targets LibreOffice `7.4`.

## Installation

### pip

lo-dev-search [PyPI](https://pypi.org/project/lo-dev-search/)

```sh
pip install lo-dev-search
```

For LibreOffice `7.3`

```sh
pip install "lo-dev-search<2.0"
```

## Finding API Documentation Online

The online API documentation can be time-consuming to search due to its great size.

If you want to have a browse, start at [LibreOffice API Namespaces](https://api.libreoffice.org/docs/idl/ref/namespaces.html), which takes a while to load.

Each Office application (e.g. Writer, Draw, Impress, Calc, Base, Math) is supported by multiple modules. For example, most of Writer's API is in Office's "text" module, while Impress' functionality comes from the "presentation" and "drawing" modules. These modules are located in [com.sun.star package](https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star.html).

Rather than searching manually through a module for a given class, it's a lot quicker to get a search engine to do it for you. This is the purpose of my `lodoc` cli, which utilizes [Google](https://google.com). For instance, at the command line, you can type:

```sh
lodoc xtext
```

and the Office API documentation on the XText interface will open in your browser.

``lodoc`` 'almost' always returns the right page, mainly because Office interfaces, and many of its services, have long unique names. (I'll explain what a service is shortly.) ``lodoc`` can be access by typing ``lodoc`` in the terminal.

Service names are less unusual, and so you should probably add the word "service" to your search. For instance, if you're looking for the Text service, type:

```sh
lodoc text service
```

Module names are also quite common words, so add "module" to the search. If you want to reach the "text" module (which implements most of Writer), search for:

```sh
lodoc text module
```

You can call lodoc with Office application names, which are mapped to API module names. For instance:

```sh
lodoc Impress
```

brings up the "presentation" module page.

## Searching the Online Developer's Guide

The online Developer's Guide can also be time-consuming to search because it's both long (around 1650 pages), and poorly organized. To help, I've written a `loguide` cli which is quite similar to `lodoc`. It calls [Google](https://google.com), limiting the search to the Developer's Guide web pages, and loads the first matching page into your web browser.

The first argument of `loguide` must be an Office application name, which restricts the search to the part of the guide focusing on that application's API or otherwise, `general`.

Type `loguide -h` for options.

General example:

```sh
loguide general Lifetime of UNO Objects
```

loads the guide page with that heading into the browser. A less precise query will probably produce the same page, but even when the result is 'wrong' it'll still be somewhere in the guide.

Impress example:

```sh
loguide impress Page Formatting
```

Calling `loguide` with just an application name, opens the guide at the start of the chapter on that topic. For example:

```sh
loguide writer
```

opens the guide at the start of the "Text Documents" chapter.

Calling `loguide` with no arguments, makes the browser load the first page of the guide.

## loapi

`loapi` uses a local database to narrow class names and namespaces for a more focused search.

### loapi comp

`loapi comp` can search for a components `const`,`enum`, `exception`, `interface`, `singleton`, `service`, `struct`, `typedef` or `any`.

Type `loapi comp -h` to see options available for `comp`.

For example:

```sh
loapi comp --search writer
Choose an option (default 1):
[0],  Cancel
[1],  UnsupportedOverwriteRequest       - com.sun.star.task.UnsupportedOverwriteRequest           - exception
[2],  LayerWriter                       - com.sun.star.configuration.backend.xml.LayerWriter      - service
[3],  ManifestWriter                    - com.sun.star.packages.manifest.ManifestWriter           - service
[4],  Writer                            - com.sun.star.xml.sax.Writer                             - service
[5],  XCompatWriterDocProperties        - com.sun.star.document.XCompatWriterDocProperties        - interface
[6],  XManifestWriter                   - com.sun.star.packages.manifest.XManifestWriter          - interface
[7],  XSVGWriter                        - com.sun.star.svg.XSVGWriter                             - interface
[8],  XWriter                           - com.sun.star.xml.sax.XWriter                            - interface
```

Choosing any number greater than `0` opens the that components url.
Option `4` would open to <https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1xml_1_1sax_1_1Writer.html>

Search can be narrowed by including `--component-type` option.

```sh
loapi comp --component-type service --search writer
Choose an option (default 1):
[0],  Cancel
[1],  LayerWriter                       - com.sun.star.configuration.backend.xml.LayerWriter      - service
[2],  ManifestWriter                    - com.sun.star.packages.manifest.ManifestWriter           - service
[3],  Writer                            - com.sun.star.xml.sax.Writer                             - service
```

A search parameter can be more that one word.

For example:

```sh
loapi comp --component-type exception --search "ill arg"
Choose an option (default 1):
[0],  Cancel
[1],  IllegalArgumentIOException        - com.sun.star.frame.IllegalArgumentIOException           - exception
[2],  IllegalArgumentException          - com.sun.star.lang.IllegalArgumentException              - exception
```

searches for all components of type `exception` that contain `ill` followed by any number of characters and then `arg`.


### loapi ns

Similar to `loapi comp`, `loapi ns` search strictly in namespaces.

Type `loapi ns -h` to see options available for `ns`.

For example:

```sh
loapi ns --search xml
Choose an option (default 1):
[0],  Cancel
[1],  com.sun.star.xml
[2],  com.sun.star.xml.crypto.sax
[3],  com.sun.star.xml.dom
[4],  com.sun.star.xml.crypto
[5],  com.sun.star.xml.xslt
[6],  com.sun.star.xml.input
[7],  com.sun.star.xml.sax
[8],  com.sun.star.xml.wrapper
[9],  com.sun.star.xml.xpath
[10], com.sun.star.xml.dom.views
```

Choosing any number greater than `0` opens the that components url.
Option `4` would open to <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1xml_1_1crypto.html>

## loproc

While developing/debugging code, it's quite easy to inadvertently trigger a runtime exception in the Office API. In the worst case, this can cause your program to exit without shutting down the *soffice* process.

`loproc --running` show if the process is running.

`loproc --kill` kills the process if it is running.

There is no issue running `loproc --kill` without running `loproc --running`.
