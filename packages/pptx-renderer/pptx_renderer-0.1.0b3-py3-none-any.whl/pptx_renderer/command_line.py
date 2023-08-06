import click
from pptx_renderer import PPTXRenderer


@click.command()
@click.option(
    "--fail_on_error",
    is_flag=True,
    help="By default, the renderer will not stop when it encouters an error while"
    " rendering a placeholder. Setting this flag will cause it to stop at the"
    " first error.",
)
@click.argument("template_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def main(fail_on_error, template_path, output_path):
    """Generate a powerpoint presentation from a template

    TEMPLATE_PATH: Path to the template file with placeholders

    OUTPUT_PATH: Path to the rendered output ppt
    """
    p = PPTXRenderer(template_path)
    p.render(output_path, {}, skip_failed=not (fail_on_error))


if __name__ == "__main__":
    main()
