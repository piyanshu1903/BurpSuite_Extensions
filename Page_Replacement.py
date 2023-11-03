from burp import IBurpExtender, IHttpListener
with open('path to dummy html file', 'r') as file:
    body1 = file.read()

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        callbacks.setExtensionName("Page_Replace Extension")
        callbacks.issueAlert("Page_Replace Active!")

    def getResponseHeadersAndBody(self, content):
        response = content.getResponse()
        response_data = self._helpers.analyzeResponse(response)
        headers = list(response_data.getHeaders() or '')
        body = response[response_data.getBodyOffset():].tostring()
        return headers, body

    def processHttpMessage(self, toolFlag, messageIsRequest, currentRequest):
        if messageIsRequest:
            return

        headers, body = self.getResponseHeadersAndBody(currentRequest)

        # Check if the response body contains the keyword "thiskeyword"
        if b"Contains this keyword or sentence" in body:

            # Replace the entire page with the content from the dummy.html file
            new_message = self._helpers.buildHttpMessage(headers, body1)
            currentRequest.setResponse(new_message)
            body=body1
        else:
            new_message = self._helpers.buildHttpMessage(headers, body)
            currentRequest.setResponse(new_message)

