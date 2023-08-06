import json
from datetime import datetime, timezone

from unpoly.adapter import BaseAdapter
from unpoly.options import Options


def test_parsing_from_request_headers():
    options = Options.parse(
        {
            "version": "2.2.1",
            "target": "[up-main~=modal]",
            "mode": "modal",
            "context": '{"test": "test"}',
            "fail_target": "[up-main~=fail]",
            "fail_mode": "fail",
            "fail_context": '{"fail": "fail"}',
            "validate": "field",
            "reload_from_time": 1608730818,
            "dismiss_layer": "null",
        },
        BaseAdapter(),
    )

    assert options.version == "2.2.1"
    assert options.target == "[up-main~=modal]"
    assert options.mode == "modal"
    assert options.context == {"test": "test"}
    assert options.fail_target == "[up-main~=fail]"
    assert options.fail_mode == "fail"
    assert options.fail_context == {"fail": "fail"}
    assert options.validate == "field"
    assert options.reload_from_time == datetime(
        2020, 12, 23, 13, 40, 18, tzinfo=timezone.utc
    )
    assert options.dismiss_layer == {}


def test_parse_broken_time():
    options = Options.parse({"reload_from_time": "no_date_time"}, BaseAdapter())
    assert options.reload_from_time == datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc)


def test_parse_broken_context():
    options = Options.parse({"context": "'a'a"}, BaseAdapter())
    assert options.context == {}


def test_parsing_with_diff():
    initial = {"existing": 1, "to_delete": True, "do_no_touch": "yes"}
    diff = {"to_delete": None, "existing": 2, "new_thing": 3}
    options = Options.parse(
        {"context": json.dumps(initial), "context_diff": json.dumps(diff)},
        BaseAdapter(),
    )
    assert options.initial_context == initial
    assert options.context_diff == diff
    assert options.context == {"existing": 2, "do_no_touch": "yes", "new_thing": 3}


def test_context_diff():
    options = Options(context={"existing": 1, "to_delete": True, "do_no_touch": "yes"})
    del options.context["to_delete"]
    options.context["existing"] = 2
    options.context["new_thing"] = 3
    assert options.context_diff == {
        "to_delete": None,
        "existing": 2,
        "new_thing": 3,
    }


def test_serialize():
    assert Options(target="target").serialize(BaseAdapter()) == {}

    options = Options(
        context={"test": "test"},
        events=[{"test": "event"}],
        title="test",
        accept_layer={},
        dismiss_layer={"test": "layer"},
    )
    options.context["change"] = "yes"  # Triggers diff rendering
    options.server_target = "new_target"  # Trigger target

    assert options.serialize(BaseAdapter()) == {
        "context": '{"change":"yes"}',  # This is just the diff!
        "events": '[{"test":"event"}]',
        "title": "test",
        "accept_layer": "null",
        "dismiss_layer": '{"test":"layer"}',
        "target": "new_target",
    }
