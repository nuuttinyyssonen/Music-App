import base64

def b64encode(data):
    return base64.b64encode(data).decode("UTF-8")