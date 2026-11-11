import urllib.parse
import zlib
import base64

def compress(xml_str):
    quoted = urllib.parse.quote(xml_str, safe='~()*!\'')
    co = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
    deflated = co.compress(quoted.encode('utf-8')) + co.flush()
    return base64.b64encode(deflated).decode('ascii')

def decompress(b64_str):
    raw = base64.b64decode(b64_str)
    inflated = zlib.decompress(raw, -15)
    return urllib.parse.unquote(inflated.decode('utf-8'))

test_xml = '<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/></root></mxGraphModel>'
c = compress(test_xml)
print("Compressed:", c[:40] + "...")
d = decompress(c)
print("Matches exactly:", d == test_xml)
