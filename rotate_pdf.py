import click
from PyPDF4 import PdfFileReader, PdfFileWriter

def rotate_pdf(path, degrees, output):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(path)
    for page in range(pdf_reader.getNumPages()):
            original = pdf_reader.getPage(page)
            pdf_writer.addPage(original.rotateClockwise(int(degrees)))
    pdf_writer.write(output)

@click.command()
@click.argument('path', type=click.File('rb'))
@click.argument('degrees')
@click.argument('output', type=click.File('wb'))
def main(path, degrees, output):
    """
    A CLI tool that rotates all the pages in a pdf 90, 180, or 270
    degrees clockwise.
    """
    rotate_pdf(path, degrees, output)

if __name__ == "__main__":
    main()
