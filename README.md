# What is it?

Program for downloading books from [website of Russian Foundation of Basic Research](https://www.rfbr.ru). 

The fact is that RFBR is a state organization, which takes money from the state in order to stimulate the development of fundamental 
science. However, it turns out that, for example, the receipt of books issued by the publisher RFBR in electronic form is prohibited. 
Only online reading is available. I think this is unfair, and this program helps to overcome this unpleasant circumstance.

# Installation

```bash
virtualenv venv -p python3
cd venv/bin
source ./activate
pip install -r <path_to_project>/requirements.txt
```

# Usage

* Go to the [search page for books published with the support of RFBR](https://www.rfbr.ru/rffi/ru/books) 
(available only in Russian version)
* Find the book you are interested in, click to its description. [Example](https://www.rfbr.ru/rffi/ru/books/o_2079247).
* Click "Read"
* Copy link and create instance of `RFBRBooksDownloader` with at least link you copied, then process it:

```python
from dowloader import RFBRBooksDownloader

obj = RFBRBooksDownloader(book_url=...)
obj.process()
```

# Additional parameters

* **output_pdf_name** (*default = 'book'*) - name of the output book pdf-file
* **delete_temporary_images** (*default = True*) - delete images saved from RFBR site, from which pdf is generated
* **requests_pause** (*default = 0.1*) - time between requests to RFBR site

# Examples

Examples of downloaded books are presented [here](https://github.com/VasilyevEvgeny/rfbr_books_downloader/tree/master/example_books)
