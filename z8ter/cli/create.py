import z8ter
from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader


env = Environment(
    loader=ChoiceLoader([
        FileSystemLoader("scaffold_dev"),
        PackageLoader("z8ter", "scaffold"),
    ]),
    autoescape=False,
    variable_start_string="[[", variable_end_string="]]",
    block_start_string="[%", block_end_string="%]",
)


def create_page(page_name: str):
    class_name = page_name.capitalize()
    page_name_lower = page_name.lower()
    template_path = z8ter.TEMPLATES_DIR / "pages" / f"{page_name_lower}.jinja"
    view_path = z8ter.VIEWS_DIR / f"{page_name_lower}.py"
    ts_path = z8ter.TS_DIR / "pages" / f"{page_name_lower}.ts"
    content_path = z8ter.BASE_DIR / "content" / f"{page_name_lower}.yaml"
    data = {"class_name": class_name, "page_name_lower": page_name_lower}
    files = [
        ("create_page_templates/view.py.j2", view_path),
        ("create_page_templates/page.jinja.j2", template_path),
        ("create_page_templates/page.yaml.j2", content_path),
        ("create_page_templates/page.ts.j2", ts_path)
    ]
    for tpl_name, out_path in files:
        tpl = env.get_template(tpl_name)
        text = tpl.render(**data)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")


def create_api(api_name: str):
    api_name_lower = api_name.lower()
    class_name = api_name.capitalize()
    data = {"api_name_lower": api_name_lower, "class_name": class_name}
    api_path = z8ter.API_DIR / f"{api_name_lower}.py"
    tpl = env.get_template("create_api_template/api.py.j2")
    text = tpl.render(**data)
    api_path.parent.mkdir(parents=True, exist_ok=True)
    api_path.write_text(text, encoding="utf-8")
