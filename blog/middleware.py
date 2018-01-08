class SimpleSubdomainMiddleware:
	def process_request(self, request):
    	host = request.META.get('HTTP_HOST', '')
	    host = host.replace('www.', '').split('.')
    	if len(host) > 2:
        	request.subdomain = ''.join(host[:-2])
	    else:
    	    request.subdomain = None
