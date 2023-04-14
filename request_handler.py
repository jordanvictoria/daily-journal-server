import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import get_single_entry, get_all_entries, update_entry, create_entry, delete_entry, get_single_mood, get_all_moods, get_entry_by_input


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        """GET."""
        self._set_headers(200)

        response = None

        parsed = self.parse_url(self.path)

        if '?' not in self.path:

            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    response = get_single_entry(id)
                else:
                    response = get_all_entries()

            if resource == "moods":
                if id is not None:
                    response = get_single_mood(id)
                else:
                    response = get_all_moods()

        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed

                # see if the query dictionary has an email key
            if resource == 'entries':
                response = get_entry_by_input(query['q'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)    
        response = None

        if resource == "entries":
            response = create_entry(post_body)

        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    def do_DELETE(self):
        """Handles DELETE requests to the server"""
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            delete_entry(id)

        self.wfile.write("".encode())

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()



def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
