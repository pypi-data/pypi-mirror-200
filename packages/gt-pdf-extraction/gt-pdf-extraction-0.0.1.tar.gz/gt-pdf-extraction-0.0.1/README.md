# PDF Extraction

**Internal Usage only.**

A pdf text/table extraction package for python.

## Installation

### via Bitbucket

```bash
pip install git+https://bitbucket.org/guangyuhe/pdf-extraction/src/main/
```

### via PyPI

```bash
pip install gt-pdf-extraction
```

## Usage

- initializing pdf extraction instance
- use method to get the result

## Arguments

- **file_path**: the path the pdf document

## Methods

- **extract_text**(_page_): extract text, _page_: int-like argument, a single page extraction or 'all' for all pages,
  default is 'all'
- **extract_table**(_mp_on_): extract table, _mp_on_: bool, whether to use multiprocess to extract tables, default is
  False
- **nr_pages**, *without ()*, return the number of pages

## Sub-methods

### extract_text

- **.apply(_func_,_args_)**: apply a function to the text, details see examples
- **str()**: return the text
- **.text**: *without ()*, return the text
- **bool()**: return True if the text is not empty

### extract_table

- **.df**: *without ()*, return the table as a pandas dataframe
- **.to_list()**: return the table as a list of list
- **.to_csv(_output_folder_)**: save the table as a csv file in the output folder

## Examples

### extract text

```python
from gt_pdf_extraction import PDFE

path: str = "/path/to/pdf"

# initialize the instance
instance = PDFE(path)

# declaring a function
extract_text = instance.extract_text(page="all")


# optional, apply a function to the text
def a_func(text, arg):
    return text.replace(arg, "")


extract_text.apply(a_func, args="a_string")

# get the text
the_text = extract_text.text  # or str(extract_text)

```

### extract table

```python
from gt_pdf_extraction import PDFE

path: str = "/path/to/pdf"

# initialize the instance
instance = PDFE(path)

# declaring a function with multiprocess enabled
extract_table = instance.extract_table(mp_on=True)

# get the table in df
the_df = extract_table.df
# get the table in list
the_list = extract_table.to_list()
# save the table as csv
extract_table.to_csv("/path/to/output/folder")

```

## Updates Log

### v0.0.1

#### initial upload

- first version

## Support

2023&copy;GoldenTech, for further support please contact author. <br>
Email: <a href="mailto:guangyu.he@golden-tech.de">guangyu.he@golden-tech.de</a>
