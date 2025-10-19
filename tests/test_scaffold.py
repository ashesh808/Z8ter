from __future__ import annotations

from z8ter.cli.new import RC_NONEMPTY_DIR, RC_OK, new_project


def test_new_project_copies_template_tree(tmp_path, capsys) -> None:
    target = tmp_path / "my_app"
    rc = new_project("ignored", path=str(target))
    captured = capsys.readouterr()

    assert rc == RC_OK
    assert "Created new Z8ter project" in captured.out
    assert (target / "templates" / "base.jinja").exists()
    assert (target / "views" / "index.py").exists()
    assert (target / "package.json").exists()


def test_new_project_rejects_nonempty_directory(tmp_path, capsys) -> None:
    target = tmp_path / "existing"
    target.mkdir()
    (target / "marker.txt").write_text("present")

    rc = new_project("ignored", path=str(target))
    captured = capsys.readouterr()

    assert rc == RC_NONEMPTY_DIR
    assert "Target directory is not empty" in captured.err
