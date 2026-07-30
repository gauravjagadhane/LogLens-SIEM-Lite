from app.parser.access_log_parser import parse_access_log, parse_log_line


COMBINED_LINE = ('192.168.1.10 - - [10/Oct/2025:13:55:36 +0000] '
                 '"GET /index.html HTTP/1.1" 200 2326 "-" "Mozilla/5.0"')


def test_parses_apache_combined_log_line():
    entry = parse_log_line(COMBINED_LINE)
    assert entry == {
        "ip": "192.168.1.10", "timestamp": "10/Oct/2025:13:55:36 +0000",
        "method": "GET", "path": "/index.html", "protocol": "HTTP/1.1",
        "status": 200, "size": 2326, "user_agent": "Mozilla/5.0",
    }


def test_stream_parser_skips_malformed_rows():
    entries = list(parse_access_log([COMBINED_LINE, "not an access log\n"]))
    assert len(entries) == 1
