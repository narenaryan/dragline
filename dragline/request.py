

class Request:
    def __init__(self,method = "GET",url=None, callback = None,meta = None,form_data = None):
        self.method = method
        self.url = url
        if url == None:
            raise Exception("url field cannot be none")
        self.callback = callback
        self.meta = meta
        self.form_data = form_data



