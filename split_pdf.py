import click
from PyPDF4 import PdfFileReader, PdfFileWriter

def format_range(pages):
    """
    Converts ranges inputted in format "n-m" or "n" into
    format required for python range function.
    """
    try:
        start, stop = pages.split('-')
        return int(start) - 1, int(stop)
    except ValueError:
        return int(pages) - 1, int(pages)

def split_pdf(input_path, page_ranges, output_name):
    for page_range in page_ranges:
        input_pdf = PdfFileReader(input_path)
        pdf_writer = PdfFileWriter()
        start, stop = format_range(page_range)
        for page in range(start, stop):
            pdf_writer.addPage(input_pdf.getPage(page))

        output = f"{output_name}_p{page_range}.pdf"
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

@click.command()
@click.argument('input_path', type=click.File('rb'), nargs=1)
@click.argument(
    'page_ranges',
    nargs=-1,
    help ='enter single page numbers or hyphen separated ranges'
)
@click.argument('output_name', nargs=1)

def main(input_path, page_ranges, output_name):
    """
    A CLI tool that splits an input pdf into specified page ranges.
    Enter the input paths, then the desired page ranges, and finally
    the output path. The output pdfs will be named 'output_name_p
    <page range>'.
    """

    split_pdf(input_path, page_ranges, output_name)

if __name__ == "__main__":
    main()
