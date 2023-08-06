# [alpha] 2023.04.03


import os
import pdfplumber


def each_process(file_path: str, page: int, queue=None):
    """
    Each read pdf process
    Args:
        file_path: (str) path to the pdf file
        page: (int) page number
        queue: used by multiprocessing module to fetch results
    Returns:
        The current page's dataframe in a list
    """

    import tabula
    from pandas.core.frame import DataFrame

    df: DataFrame = DataFrame()
    try:
        df = tabula.read_pdf(file_path, pages=page, stream=True, pandas_options={'header': None})[0]
        # df = tabula.read_pdf(file_path, pages=page, pandas_options={'header': None})[0]
        # df = tabula.read_pdf(file_path, pages=page, lattice=True, pandas_options={'header': None})[0]
    except IndexError:
        # There was no table extracted from the last page
        pass

    if queue is None:
        return [df]
    else:
        queue.put(df)


class PDFE:

    def __init__(self, file_path: str):
        """
        Args:
            file_path (str): path to the document
        """

        self.file_path: str = file_path
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"'{self.file_path}' not found")

        self.nr_pages: int = 0
        with pdfplumber.open(self.file_path) as pdf:
            self.nr_pages = len(pdf.pages)

    def extract_text(self, page="all"):
        """
        Extract text from a pdf file using ExtractText class with pdfplumber
        Args:
            page: page number, 'all' stands for all pages, int or int-like string is accepted
        Returns:
            ExtractText object
        """
        return self.ExtractText(self.file_path, self.nr_pages, page)

    def extract_table(self, mp_on: bool = False):
        """
        Extract table (dataframe) from a pdf file using ExtractTable class with tabula-py
        Returns:
            ExtractTable object
        """
        return self.ExtractTable(self.file_path, self.nr_pages, mp_on)

    class ExtractText:
        def __init__(self, file_path: str, nr_pages: int, page: int or str = "all"):
            """
            Extract text from a pdf file using pdfplumber
            Args:
                file_path: (str) path to the pdf file, should be inherited from the parent class
                nr_pages: (int) number of pages in the pdf file, should be inherited from the parent class
                page: should be inherited from the parent class
            """

            self.file_path: str = file_path

            self.nr_pages: int = nr_pages
            self.page: int or str = page

            self.text_each_page: list = self.convert_to_text()
            self.text: str = "\n".join(self.text_each_page)

        def __repr__(self):
            return f"ExtractText({self.file_path})"

        def __str__(self):
            return self.text

        def __bool__(self):
            return bool(self.text_each_page)

        def convert_to_text(self) -> list:
            returned_text: list[str] = []
            page_str: str
            if self.page == "all":
                with pdfplumber.open(f'{self.file_path}') as pf:
                    for page in pf.pages:
                        page_str = page.extract_text()
                        returned_text.append(page_str)
            else:
                try:
                    page = int(self.page)
                except ValueError:
                    raise ValueError(f"page number must be 'all' or page number, not '{self.page}'")
                if 0 < page <= self.nr_pages:
                    i: int = 0
                    with pdfplumber.open(f'{self.file_path}') as pf:
                        for each_page in pf.pages:
                            if i == page - 1:
                                page_str = each_page.extract_text()
                                returned_text.append(page_str)
                            i += 1
                else:
                    raise ValueError(f"invalid page number: '{page}'")

            return returned_text

        def apply(self, func, *args, **kwargs):
            """
            Apply a function to each page's text
            Args:
                func: the raw function to be applied
                *args: arguments for the function (except the first string input argument)
                **kwargs: keyword arguments for the function (except the first string input argument)
            """

            self.text_each_page = [func(each_page, *args, **kwargs) for each_page in self.text_each_page]
            self.text = "\n".join(self.text_each_page)

    class ExtractTable:

        def __init__(self, file_path: str, nr_pages: int, mp_on: bool = False):
            """
            Extract table (dataframe) from a pdf file using tabula-py
            Args:
                file_path: (str) path to the pdf file, should be inherited from the parent class
                nr_pages: (int) number of pages in the pdf file, should be inherited from the parent class
                mp_on: (bool) whether to use multiprocessing to speed up the process
            """

            self.file_path: str = file_path
            self.mp_on: bool = mp_on

            self.nr_pages: int = nr_pages

            self.df = self.convert_to_df()

        def convert_to_df(self):
            """
            Creating a dataframe from the input pdf
            Returns:
                A converted dataframe
            """

            import pandas as pd

            returned_df: list = []
            if self.mp_on:
                # to enable multiprocessing, please install the gy-multiprocessing package beforehand
                # TODO! mp is not working in complied excutable file
                from gy_multiprocessing.multiprocessing import multi_process as gymp

                # Multiprocessing can reduce the processing time for 18 pages from 24 to 11 seconds
                mp = gymp.MultiProcess(silent=True)
                for each_page in range(1, self.nr_pages + 1):
                    arg: tuple = (self.file_path, each_page)
                    mp.add(each_process, arg)
                returned_df = mp.run()
            else:
                for each_page in range(1, self.nr_pages + 1):
                    returned_df += each_process(self.file_path, each_page)
                    print(f"Page {each_page} done")

            result_df = pd.concat(returned_df, ignore_index=True)

            return result_df

        def to_csv(self, output_folder: str):
            """
            Convert the input pdf to csv files
            Args:
                output_folder: (str) The FOLDER path to the output CSV, csv will be named as "CPSD_{input_file_name}.csv"
            """

            if ".csv" in output_folder:
                print(
                    f"Your are typing a file name, not a folder name, "
                    f"the output file will be saved in the same folder as your input file")
                output_folder = os.path.dirname(output_folder)
            else:
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

            # CPSD: converted pdf source data
            output_file: str = os.path.join(output_folder,
                                            "CPSD_" + os.path.basename(self.file_path).replace(".pdf", ".csv"))

            self.df.rename(columns=self.df.iloc[0]) \
                .drop(self.df.index[0]) \
                .to_csv(output_file, index=False)

        def to_list(self) -> list:
            """
            Convert the input pdf to a list object
            Returns:
                A converted list
            """

            return self.df.values.tolist()
