import pathlib

import click

import orjson


@click.option(
    "--input",
    type=click.File(
        mode="rb",
    ),
    required=True,
)
@click.option(
    "--output",
    type=click.Path(
        dir_okay=True,
        path_type=pathlib.Path,
    ),
    required=True,
)
@click.command()
def main(
    input,
    output,
):
    data = orjson.loads(input.read())

    for type in data:
        click.echo(f"Generating {type}...")
        if "indexes" not in data[type]:
            raise ValueError(f"indexes not found in {type}")
        if "objects" not in data[type]:
            raise ValueError(f"objects not found in {type}")

        for index in data[type]["indexes"]:
            click.echo(f" - Generating {index}...")

            for obj in [obj for obj in data[type]["objects"] if index in obj]:
                (output / type / index / obj[index].lower()).mkdir(parents=True, exist_ok=True)
                with open(output / type / index / obj[index].lower() / "index.json", "wb") as f:
                    f.write(orjson.dumps(obj, option=orjson.OPT_SORT_KEYS))
                click.echo(
                    f"   - Generated {output / type / index / obj[index].lower() / 'index.json'}"
                )


if __name__ == "__main__":
    main()
