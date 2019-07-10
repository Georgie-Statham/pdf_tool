import click
from PyPDF4 import PdfFileReader, PdfFileWriter

def join_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

        pdf_writer.write(output)

@click.command()
@click.argument('paths', type=click.File('rb'), nargs=-1)
@click.argument('output', type=click.File('wb'), nargs=1)
def main(paths, output):
    """
    A cli tool that joins an unlimited number of pdfs together.
    Enter the paths of the pdfs to be joined in the order they will
    appear in the output pdf, and end with the output path.
    """

    join_pdfs(paths, output)

if __name__ == "__main__":
    main()
