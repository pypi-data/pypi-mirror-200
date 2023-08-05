"""tests for more kinds of contents"""
import json

import pytest


@pytest.mark.parametrize(
    "allow_hidden,expect_success,expect_content,extra_ignore",
    [
        [True, True, True, []],
        [False, False, False, []],
        [False, True, False, [r"/\.binder/"]],
    ],
)
def test_contents_with_dot(
    allow_hidden,
    expect_success,
    expect_content,
    extra_ignore,
    an_empty_lite_dir,
    script_runner,
):
    """Can hidden files be exposed with contents?"""
    config = {
        "LiteBuildConfig": {
            "ignore_sys_prefix": True,
            "extra_ignore_contents": extra_ignore,
        },
        "ContentsManager": {"allow_hidden": allow_hidden},
    }
    print("config", config)
    (an_empty_lite_dir / "jupyter_lite_config.json").write_text(json.dumps(config))
    dot_binder = an_empty_lite_dir / ".binder"
    dot_binder.mkdir()
    postbuild = dot_binder / "postBuild"
    postbuild.write_text("#!/usr/bin/env bash\necho ok")

    result = script_runner.run(
        "jupyter",
        "lite",
        "build",
        "--contents",
        ".",
        cwd=str(an_empty_lite_dir),
    )
    if expect_success:
        assert result.success
    else:
        assert not result.success
        assert "jupyter_lite_config" in result.stdout

    out = an_empty_lite_dir / "_output"
    root_contents_json = out / "api/contents/all.json"
    out_postbuild = out / "files/.binder/postBuild"
    hidden_contents_json = out / "api/contents/.binder/all.json"

    if expect_content:
        root_contents = json.loads(root_contents_json.read_text(encoding="utf-8"))
        assert len(root_contents["content"]) == 1, root_contents
        assert out_postbuild.exists()

        hidden_contents = json.loads(hidden_contents_json.read_text(encoding="utf-8"))

        postbuild_content = hidden_contents["content"][0]
        assert postbuild_content["name"] == "postBuild", postbuild_content
        assert postbuild_content["path"] == ".binder/postBuild", postbuild_content
    else:
        assert not root_contents_json.exists()
