import argparse
from time import sleep

from rich.console import Console

from services.template_service import TemplateService


def get_template(problem_slug: str, lang: str):
    template_service = TemplateService()

    template = template_service.get_template(problem_slug, lang)

    return template


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("problem_slug", type=str, help="The problem slug to retrieve")
    parser.add_argument("lang", type=str, help="The language template to use")
    args = parser.parse_args()

    console = Console()

    console.print(
        f"[white]Retrieving item with ID {args.problem_slug} and language {args.lang}...[/white]"
    )

    template = get_template(args.problem_slug, args.lang)

    filename = console.input(
        "[blue]Enter the filename to save your template code[/blue]: "
    )

    with open(filename, "w") as fd:
        fd.write(template)

    console.print("[green]Done![/green]")


if __name__ == "__main__":
    main()
