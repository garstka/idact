from idact.detail.nodes.get_node_memory_usage \
    import parse_top_res_format_to_kib


def test_parse_top_res_format_to_kib():
    assert parse_top_res_format_to_kib("234243") == 234243
    assert parse_top_res_format_to_kib("0.021m") == 21
    assert parse_top_res_format_to_kib("0.021g") == 22020
    assert parse_top_res_format_to_kib("0.021t") == 22548578
    assert parse_top_res_format_to_kib("0.001p") == 1099511627
