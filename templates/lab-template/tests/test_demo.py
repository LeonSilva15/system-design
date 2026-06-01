from lab_template.demo import run_demo


def test_demo_has_observable_output() -> None:
    output = run_demo()

    assert output
    assert any(line.startswith("summary=") for line in output)
