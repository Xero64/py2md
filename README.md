# py2md

Run python code in Jupyter to generate markdown reports.

**Usage:**

```
py2md test_py2md.py
```

This will then run Jupyter and generate a md file output with associated images.

**Debug Usage:**

```
py2md test_py2md.py -debug
```

This will also print out all Jupyter output to see if anything is missing from the output.

**No Code, No Cell Headers and inline images Usage:**

```
py2md test_py2md.py -nocode -nohead -inline
```

This will hide the python code block as well as cell headers and all images will be part of the markdown file as html code.
