import pathlib

import click

import orjson

@click.group()
def main():
    pass

@click.argument("index", type=str)
@click.argument("type", type=str)
@click.argument("input", type=click.File(mode='r'))
@main.command()
def targets(
    index,
    type,
    input,
):
    data = orjson.loads(input.read())

    if type not in data:
        raise ValueError(f"{type} not found in data")

    seen = {}
    for obj in {obj[index].lower() for obj in data[type] if index in obj}:
        if obj in seen:
            raise ValueError(f"Duplicate {index} found: {obj} in {type}")
        print(obj)


@click.argument("index", type=str)
@click.argument("type", type=str)
@click.argument("input", type=click.File(mode='r'))
@click.option("--output", type=click.Path(dir_okay=True, path_type=pathlib.Path), required=False, default=pathlib.Path("."))
@main.command()
def generate(
    index,
    type,
    input,
    output
):
    data = orjson.loads(input.read())

    if type not in data:
        raise ValueError(f"{type} not found in data")

    for obj in [obj for obj in data[type] if index in obj]:
        (output / type / index / obj[index].lower()).mkdir(parents=True, exist_ok=True)
        with open(output / type / index / obj[index].lower() / "index.json", "wb") as f:
            f.write(orjson.dumps(obj, option=orjson.OPT_SORT_KEYS))
        click.echo(f"Generated {output / type / index / obj[index].lower() / 'index.json'}")

if __name__ == "__main__":
    main()
