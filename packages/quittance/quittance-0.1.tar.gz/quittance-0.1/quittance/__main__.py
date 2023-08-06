#!/usr/bin/env python3

from pathlib import Path
from datetime import date, timedelta
import sys
import json
import locale
from argparse import ArgumentParser

from weasyprint import HTML
from jinja2 import Environment, PackageLoader, select_autoescape
import tomlkit as toml


def parse_args():
    parser = ArgumentParser(description="Génère une quittance de loyer")
    subparsers = parser.add_subparsers(required=False)

    parser_conf = subparsers.add_parser(
        "config",
        help="Quittance configuration. Run without argument to see the current configuration.",
    )
    parser_conf.add_argument("--bailleur-name", metavar="'Ano Nymous'")
    parser_conf.add_argument("--bailleur-address", metavar="'10 route de la corniche'")
    parser_conf.add_argument("--bailleur-code-postal", metavar="69000")
    parser_conf.add_argument("--bailleur-city", metavar="'Lyon'")
    parser_conf.add_argument("--bailleur-country", metavar="'France'")
    parser_conf.add_argument("--locataire-name", metavar="'Ano Nymous'")
    parser_conf.add_argument("--locataire-address", metavar="'10 route de la corniche'")
    parser_conf.add_argument("--locataire-code-postal", metavar="'69000'")
    parser_conf.add_argument("--locataire-city", metavar="'Lyon'")
    parser_conf.add_argument("--locataire-country", metavar="'France'")
    parser_conf.add_argument("--dernier-numero", type=int, metavar="123")
    parser_conf.add_argument("--loyer-hors-charges", type=int, metavar="123")
    parser_conf.add_argument("--charges", type=int, metavar="123")
    parser_conf.set_defaults(func=main_config)

    parser.set_defaults(func=main_new)

    return parser.parse_args()


def main():
    args = parse_args()
    func = args.func
    del args.func
    return func(args)


def load_config():
    try:
        with open(Path.home() / ".config" / "quittance.toml", "r") as f:
            config = toml.load(f)
    except FileNotFoundError:
        config = {}
    return config


def save_config(config):
    with open(Path.home() / ".config" / "quittance.toml", "w") as f:
        toml.dump(config, f)


def main_config(args):
    keys = set(vars(args).keys())
    args = {key: value for key, value in vars(args).items() if value is not None}
    config = load_config()
    config.update(args)
    if "dernier_numero" not in config:
        config["dernier_numero"] = 0
    for missing_key in sorted(keys - set(config)):
        config[missing_key] = ""
    save_config(config)
    print(
        f"You can edit the configuration file: {Path.home() / '.config' / 'quittance.toml'}"
    )
    print(toml.dumps(config))


def get_prev_month():
    today = date.today()
    first_of_month = today.replace(day=1)
    last_day_of_last_month = first_of_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)
    return f"du {first_day_of_last_month:%A %d %B %Y} au {last_day_of_last_month:%A %d %B %Y}"


def main_new(args):
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
    env = Environment(loader=PackageLoader("quittance"), autoescape=select_autoescape())
    template = env.get_template("quittance.html")
    config = load_config()

    env = config.copy()

    env["date"] = date.today().strftime("%A %d %B %Y")
    env["periode"] = get_prev_month()

    config["dernier_numero"] += 1
    env["quittance_no"] = config["dernier_numero"]
    save_config(config)

    output = f"{date.today():%Y-%m-%d} quittance-{env['quittance_no']}.pdf"
    HTML(
        string=template.render(**env), base_url=str(Path(template.filename).parent)
    ).write_pdf(output)
    print("Nouvelle quittance :", output)


if __name__ == "__main__":
    main()
