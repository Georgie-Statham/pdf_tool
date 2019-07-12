import click
from PyPDF4 import PdfFileReader, PdfFileWriter
import re

# Parameter classes

class PageRange(click.ParamType):
    name = 'page-range'

    def convert(self, value, param, ctx):
        page_range = re.match(r'\d+-\d+', value)
        single_page = re.match(r'\d+', value)

        if not (page_range or single_page):
            self.fail(
                f'{value} is not a valid page range.',
                param,
                ctx,
            )

        return value

class DegreesRotate(click.ParamType):
    name = 'rotate-degrees'

    def convert(self, value, param, ctx):
        found = False
        if value == '90' or value == '180' or value == '270':
            found = True

        if not found:
            self.fail(
                f'{value} is not 90, 180, or 270.',
                param,
                ctx,
            )

        return value

# Helper functions

def format_range(pages):
    """
    Converts strings of form "n-m" or "n" into
    format required for python range function.
    """
    try:
        start, stop = pages.split('-')
        return int(start) - 1, int(stop)
    except ValueError:
        return int(pages) - 1, int(pages)


@click.group()
def main():
    """
    A CLI tool with sub-commands that allow you to join, split
    and rotate pdfs.
    """
    pass


@main.command()
@click.argument('paths', type=click.File('rb'), nargs=-1)
@click.argument('output', type=click.File('wb'), nargs=1)
def join(paths, output):
    """
    Joins an unlimited number of pdfs together.
    Enter the paths of the pdfs to be joined in the order they will
    appear in the output pdf, and end with the output path.
    """

    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

        pdf_writer.write(output)


@main.command()
@click.argument('input_path', type=click.File('rb'), nargs=1)
@click.argument('page_ranges', type=PageRange(), nargs=-1)
@click.argument('output_name', type=str, nargs=1)
def split(input_path, page_ranges, output_name):
    """
    Extracts the specified page ranges from a pdf.
    Enter the input paths, then the desired page ranges (as single page numbers or hyphen separated ranges) and finally the output path.
    The output pdfs will be named '<output_name>_p<page_range>'.
    """

    for page_range in page_ranges:
        input_pdf = PdfFileReader(input_path)
        pdf_writer = PdfFileWriter()
        start, stop = format_range(page_range)
        for page in range(start, stop):
            pdf_writer.addPage(input_pdf.getPage(page))

        output = f"{output_name}_p{page_range}.pdf"
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)


@main.command()
@click.argument('path', type=click.File('rb'))
@click.argument('degrees', type=DegreesRotate())
@click.argument('output', type=click.File('wb'))
def rotate(path, degrees, output):
    """
    Rotates all the pages in a pdf 90, 180, or 270 degrees clockwise.
    Enter the input path, then the degrees clockwise
    you want the pdf to be rotated, then the output path.
    """

    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(path)

    for page in range(pdf_reader.getNumPages()):
            original = pdf_reader.getPage(page)
            pdf_writer.addPage(original.rotateClockwise(int(degrees)))
    pdf_writer.write(output)


if __name__ == "__main__":
    main()
