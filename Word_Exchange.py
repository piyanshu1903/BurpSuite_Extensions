from burp import IBurpExtender, IHttpListener

class BurpExtender(IBurpExtender, IHttpListener):
  def registerExtenderCallbacks(self, callbacks):
    self._callbacks = callbacks
    self._helpers = callbacks.getHelpers()
    callbacks.registerHttpListener(self)
    callbacks.setExtensionName("Word_Exchange")
    callbacks.issueAlert("Word_Exchange Active !")

  def getResponseHeadersAndBody(self, content):
    response = content.getResponse()
    response_data = self._helpers.analyzeResponse(response)
    headers = list(response_data.getHeaders() or '')
    body = response[response_data.getBodyOffset():].tostring()
    return headers, body

  def processHttpMessage(self, tool, is_request, content):
    if is_request:
      return
    headers, body = self.getResponseHeadersAndBody(content)

    # modify body
    body = body.replace("cloud", "nothing")

    new_message = self._helpers.buildHttpMessage(headers, body)
    content.setResponse(new_message)