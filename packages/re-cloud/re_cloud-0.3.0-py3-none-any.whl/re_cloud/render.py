from jinja2 import Template
from tempfile import NamedTemporaryFile, TemporaryDirectory
import os
import shutil


def render_markdown(to_upload):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "templates/markdown.html.j2")

    with open(template_path) as template_file:
        template_file = template_file.read()
        with open(to_upload) as data_file:
            data = data_file.read()

            rendered = Template(template_file).render(content=data)
            tf = NamedTemporaryFile(delete=False)
            tf.write(rendered.encode("utf-8"))
            tf.close()

    return tf.name


def render_pdf(pdf_file):
    # Produces a HTML file which shows the PDF
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "templates/pdf.html.j2")
    with open(template_path) as template_file:
        render = Template(template_file.read()).render(pdf_file=pdf_file)

        td = TemporaryDirectory()

        with open(os.path.join(td.name, "index.html"), "w") as f:
            f.write(render)

        shutil.copy(pdf_file, td.name)

    return td


def render_csv(to_upload):
    pass
    # Using
