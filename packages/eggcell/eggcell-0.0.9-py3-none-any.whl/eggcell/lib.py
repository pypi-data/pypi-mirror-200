import dataclasses
import io
import logging
import pathlib

import jinja2
import pkg_resources

_logger = logging.getLogger(__name__)

package = __name__.split(".")[0]
TEMPLATES_PATH = pathlib.Path(pkg_resources.resource_filename(package, "templates/"))
loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
env = jinja2.Environment(loader=loader, keep_trailing_newline=True)


@dataclasses.dataclass
class Shell:
    name: str
    want: bool
    extension: str


def want_shell(shell_name: str, shells: list[str]):
    for shell_iter in shells:
        if shell_name in shell_iter.lower():
            return True
    return False


def get_shell_preferences(shell_names: list[str]) -> list[Shell]:
    shells = []

    name = "bash"
    s = Shell(name, want_shell(name, shell_names), extension="sh")
    shells.append(s)

    name = "powershell"
    s = Shell(name, want_shell(name, shell_names), extension="ps1")
    shells.append(s)

    return shells


def get_prefered_templates(
    shells: list[Shell], template_fnames: list[str]
) -> list[str]:
    filtered_template_fnames = []
    for shell in shells:
        for fname in template_fnames:
            path = pathlib.Path(fname)
            path_tmp = path.stem.replace(".j2", "")

            if shell.want and path_tmp.lower().endswith(shell.extension):
                filtered_template_fnames.append(fname)

    return filtered_template_fnames


def aggregate_templates_to_str(templates: list[str], template_data: dict) -> str:
    vfile = io.StringIO()
    vfile.write("#" + "-" * 10)
    vfile.write("\n")

    for fname in templates:
        template = env.get_template(fname)
        rendered = template.render(data=template_data)
        trimmed = rendered.strip()
        out = f"{trimmed}\n"
        vfile.write(out)
        vfile.write("\n")

    return vfile.getvalue()


def fix_ordering(l1, l2):
    fnames = []
    for tpl in l1:
        if tpl in l2:
            fnames.append(tpl)
    return fnames


def get_all_templates():
    # I prefer these to have priority,
    # the others can come in any oreder
    template_fnames = [
        "bash1.sh.j2",
        "pwsh.ps1.j2",
    ]
    for path in list(TEMPLATES_PATH.glob("*.j2")):
        if path.name not in template_fnames:
            template_fnames.append(path.name)

    return template_fnames


def main(args):
    shell_names = args.shells
    user_variables = args.variables

    template_fnames = get_all_templates()
    shells = get_shell_preferences(shell_names)
    filtered_fnames = get_prefered_templates(shells, template_fnames)
    template_fnames = fix_ordering(template_fnames, filtered_fnames)

    data = {"variables": user_variables}
    out = aggregate_templates_to_str(template_fnames, template_data=data)
    print(out)
    _logger.info("Script ends here")
