from urllib.parse import parse_qsl

ts = 'section=東區&name=奇沐'

print(parse_qsl(ts))