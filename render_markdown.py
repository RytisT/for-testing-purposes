#!/usr/bin/env python

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from models import GithubToken, Account
from constant import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
from helpers import validate_jwt_token, get_jwt_token, handle_404, handle_unauthorized, transform_html, compile_html
import os



import logging
import endpoints
import webapp2
import json
import re
import pdb



class GetGithubMarkdown(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        user = self.request.get('user')
        repo = self.request.get('repo')
        branch = self.request.get('branch')
        path = self.request.get('path')

        id = self.request.get('id')
        jwt = get_jwt_token(request=self.request)

        payload = validate_jwt_token(jwt)
        client_key = payload.get('iss')

        if not user or not repo or not branch or not path:
            if not url:
                raise endpoints.BadRequestException("You must specify parameters user, repo, branch and path")
            match = re.search('.*github.com/(.*?)/(.*?)/(?:blob|raw)/(.*?)/(.*?)(?:\?|$)', url)
            if not match:
                match = re.search('.*githubusercontent.com/(.*?)/(.*?)/(.*?)/(.*?)(?:\?|$)', url)

            if not match:
                raise endpoints.BadRequestException("Incorrect Markdown File URL provided")
            user, repo, branch, path = match.group(1, 2, 3, 4)

        headers = {}
        if id:
            token_key = ndb.Key(urlsafe=id)
            if token_key is None:
                handle_404(self.response, "A Github token is required to pull markdown.")
                return
            token = token_key.get()
            if token is None:
                handle_404(self.response, "Github token not found.")
                return

            if token.client_key != client_key:
                raise endpoints.UnauthorizedException("Token client key does not match account client key.")

            headers = {'Authorization': 'token %s' % token.token_value}

        url = "https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}".format(user=user,
                                                                                       repo=repo,
                                                                                       branch=branch,
                                                                                       path=path)
        try:
            result = urlfetch.fetch(url, headers=headers)
            if result.status_code == 200:
                self.response.out.write(result.content)
            else:
                self.response.status = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        self.response.headers.add_header("Content-Type", "text/plain; charset=utf-8")


class GetMarkdownStatic(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        user = self.request.get('user')
        repo = self.request.get('repo')
        branch = self.request.get('branch')
        path = self.request.get('path')

        id = self.request.get('id')
        jwt = get_jwt_token(request=self.request)


        payload = validate_jwt_token(jwt)
        client_key = payload.get('iss')

        if not user or not repo or not branch or not path:
            if not url:
                raise endpoints.BadRequestException("You must specify parameters user, repo, branch and path")
            match = re.search('.*github.com/(.*?)/(.*?)/(?:blob|raw)/(.*?)/(.*?)(?:\?|$)', url)
            if not match:
                match = re.search('.*githubusercontent.com/(.*?)/(.*?)/(.*?)/(.*?)(?:\?|$)', url)

            if not match:
                raise endpoints.BadRequestException("Incorrect Markdown File URL provided")
            user, repo, branch, path = match.group(1, 2, 3, 4)

        headers = {}
        if id:
            token_key = ndb.Key(urlsafe=id)
            if token_key is None:
                handle_404(self.response, "A Github token is required to pull markdown.")
                return
            token = token_key.get()
            if token is None:
                handle_404(self.response, "Github token not found.")
                return

            if token.client_key != client_key:
                raise endpoints.UnauthorizedException("Token client key does not match account client key.")

            headers = {'Authorization': 'token %s' % token.token_value}

        url = "https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}".format(user=user,
                                                                                       repo=repo,
                                                                                       branch=branch,
                                                                                       path=path)
        try:
            result = urlfetch.fetch(url, headers=headers)
            if result.status_code == 200:
                html = transform_html(result.content, url)
                self.response.out.write(html)
            else:
                self.response.status = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        self.response.headers.add_header("Content-Type", "text/html; charset=utf-8")


class GetGithubIssues(webapp2.RequestHandler):
    def get(self):
        user = self.request.get('user')
        repo = self.request.get('repo')
        query = self.request.get('query')

        id = self.request.get('id')
        jwt = get_jwt_token(request=self.request)

        if not user or not repo:
            raise endpoints.BadRequestException("You must specify parameters user, repo, branch and path")

        if not id:
            raise endpoints.BadRequestException("You must specify the parameter, id.")

        token_key = ndb.Key(urlsafe=id)
        token = token_key.get()
        if token is None:
            handle_404(self.response, "Github token not found.")
            return

        payload = validate_jwt_token(jwt)
        client_key = payload.get('iss')

        if token.client_key != client_key:
            raise endpoints.UnauthorizedException("Token client key does not match account client key.")
        url = "https://api.github.com/repos/{user}/{repo}/issues?{query}".format(user=user,
                                                                                 repo=repo,
                                                                                 query=query)
        try:
            result = urlfetch.fetch(url, headers={'Authorization': 'token %s' % token.token_value,
                                                  'Content-Type': 'application/x-www-form-urlencoded'})
            if result.status_code == 200:
                issues = [issue for issue in json.loads(result.content) if "pull_request" not in issue.keys()]
                open_issues = len([issue for issue in issues if issue["state"] == "open"])
                issue_data = {
                    "issues": issues,
                    "open": open_issues,
                    "closed": len(issues) - open_issues,
                    "query": query,
                    "query_url": "https://github.com/{user}/{repo}/issues?{query}&q=is%3Aissue".format(user=user,
                                                                                                       repo=repo,
                                                                                                       query=query)
                }
                self.response.out.write(json.dumps(issue_data))
            else:
                self.response.status = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        self.response.headers["Content-Type"] =  "application/json"


class GetGithubPullRequests(webapp2.RequestHandler):
    def get(self):
        user = self.request.get('user')
        repo = self.request.get('repo')
        query = self.request.get('query')

        id = self.request.get('id')
        jwt = get_jwt_token(request=self.request)

        if not user or not repo:
            raise endpoints.BadRequestException("You must specify parameters user, repo, branch and path")

        if not id:
            raise endpoints.BadRequestException("You must specify the parameter, id.")

        token_key = ndb.Key(urlsafe=id)
        token = token_key.get()
        if token is None:
            handle_404(self.response, "Github token not found.")
            return

        payload = validate_jwt_token(jwt)
        client_key = payload.get('iss')

        if token.client_key != client_key:
            raise endpoints.UnauthorizedException("Token client key does not match account client key.")
        url = "https://api.github.com/repos/{user}/{repo}/pulls?{query}".format(user=user,
                                                                                repo=repo,
                                                                                query=query)
        try:
            result = urlfetch.fetch(url, headers={'Authorization': 'token %s' % token.token_value,
                                                  'Content-Type': 'application/x-www-form-urlencoded'})
            if result.status_code == 200:
                pull_requests = json.loads(result.content)
                open_prs = len([pr for pr in pull_requests if pr["state"] == "open"])
                pr_data = {
                    "issues": pull_requests,
                    "open": open_prs,
                    "closed": len(pull_requests) - open_prs,
                    "query": query,
                    "query_url": "https://github.com/{user}/{repo}/issues?{query}&q=is%3Apr".format(user=user,
                                                                                                    repo=repo,
                                                                                                    query=query)
                }
                self.response.out.write(json.dumps(pr_data))
            else:
                self.response.status = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        self.response.headers["Content-Type"] = "application/json"


class GetGithubFile(webapp2.RequestHandler):
    def get(self):
        user = self.request.get('user')
        repo = self.request.get('repo')
        branch = self.request.get('branch')
        path = self.request.get('path')

        id = self.request.get('id')
        jwt = get_jwt_token(request=self.request)

        if not user or not repo or not branch or not path:
            raise endpoints.BadRequestException("You must specify parameters user, repo, branch and path")

        if not id:
            raise endpoints.BadRequestException("You must specify the parameter, id.")

        token_key = ndb.Key(urlsafe=id)
        token = token_key.get()
        if token is None:
            handle_404(self.response, "Github token not found.")
            return

        payload = validate_jwt_token(jwt)
        client_key = payload.get('iss')

        if token.client_key != client_key:
            raise endpoints.UnauthorizedException("Token client key does not match account client key.")
        url = "https://api.github.com/repos/{user}/{repo}/contents/{path}?ref={branch}".format(user=user,
                                                                                               path=path,
                                                                                               repo=repo,
                                                                                               branch=branch)
        try:
            result = urlfetch.fetch(url, headers={'Authorization': 'token %s' % token.token_value,
                                                  'Accept': 'application/vnd.github.v3.json'})
            if result.status_code == 200:
                file_data = json.loads(result.content)
                content = file_data['content'].decode('base64')
                # pdb.set_trace()
                pr_data = {
                    "content": content,
                    "size": file_data['size'],
                    "name": file_data['name'],
                    "url": file_data['html_url'],
                    "length": len(content.splitlines())
                }
                self.response.out.write(json.dumps(pr_data))
            else:
                self.response.status = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        self.response.headers["Content-Type"] = "application/json"


class GetGithubFileStatic(webapp2.RequestHandler):
    def get(self):
        user = self.request.get('user')
        repo = self.request.get('repo')
        branch = self.request.get('branch')
        path = self.request.get('path')

        id = self.request.get('token')
        jwt = get_jwt_token(request=self.request)

        if not user or not repo or not branch or not path:
            raise endpoints.BadRequestException("You must specify parameters user, repo, branch and path")

        if not id:
            raise endpoints.BadRequestException("You must specify the parameter, id.")

        token_key = ndb.Key(urlsafe=id)
        token = token_key.get()
        if token is None:
            handle_404(self.response, "Github token not found.")
            return

        payload = validate_jwt_token(jwt)
        client_key = payload.get('iss')

        if token.client_key != client_key:
            raise endpoints.UnauthorizedException("Token client key does not match account client key.")
        url = "https://api.github.com/repos/{user}/{repo}/contents/{path}?ref={branch}".format(user=user,
                                                                                               path=path,
                                                                                               repo=repo,
                                                                                               branch=branch)
        try:
            result = urlfetch.fetch(url, headers={'Authorization': 'token %s' % token.token_value,
                                                  'Accept': 'application/vnd.github.v3.json'})
            if result.status_code == 200:
                file_data = json.loads(result.content)
                content = file_data['content'].decode('base64')
                content = "import markdown\nimport markdown\n\nimport markdown\n"
                pr_data = {
                    "content": content,
                    "size": file_data['size'],
                    "name": file_data['name'],
                    "url": file_data['html_url'],
                    "length": len(content.splitlines())
                }
                template = os.path.join(os.path.dirname(__file__), 'templates/file-template.html')
                with open(template,'r') as f:
                    source = f.read().decode("utf-8")
                html = compile_html(source, pr_data)
                self.response.out.write(html)
            else:
                self.response.status = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        self.response.headers["Content-Type"] = "text/html"


class AddOnInstalledCallback(webapp2.RequestHandler):
    def post(self):
        jsonstring = self.request.body
        jsonobject = json.loads(jsonstring)
        addon_key = jsonobject.get("key")
        client_key = jsonobject.get('clientKey')
        shared_secret = jsonobject.get('sharedSecret')
        base_url = jsonobject.get('baseUrl')
        jwt = get_jwt_token(request=self.request)

        account = Account.get_by_id(id=client_key)
        if jwt and account:
            payload = validate_jwt_token(jwt)
            jwt_client_key = payload.get('iss')

            if client_key != jwt_client_key:
                handle_unauthorized(self.response, "You are not authorized")

            account = Account(addon_key=addon_key, client_key=client_key, shared_secret=shared_secret,
                              base_url=base_url, id=client_key)
            account.put()

        elif account is None:
            account = Account(addon_key=addon_key, client_key=client_key, shared_secret=shared_secret,
                              base_url=base_url, id=client_key)
            account.put()
        else:
            handle_unauthorized(self.response, "You are not authorized")


class GithubAuthorize(webapp2.RequestHandler):
    def get(self):
        code = self.request.get('code')
        jwt = get_jwt_token(request=self.request)
        token_name = self.request.get('tokenName')
        config_url = self.request.get('configPageUrl')

        if not jwt:
            raise endpoints.UnauthorizedException("Authorization token not specified.")

        if not code:
            raise endpoints.BadRequestException("You must specify the Github code.")

        if not token_name:
            raise endpoints.BadRequestException("You must specify a token name.")

        payload = validate_jwt_token(jwt)
        client_key = payload.get('iss')

        url = "https://github.com/login/oauth/access_token?code={code}&client_id={client_id}&client_secret={client_secret}"

        try:
            result = urlfetch.fetch(url.format(code=code, client_id=GITHUB_CLIENT_ID,
                                               client_secret=GITHUB_CLIENT_SECRET),
                                    method=urlfetch.POST, headers={"Accept": "application/json"})
            if result.status_code == 200:
                jsonobject = json.loads(result.content)
                # todo check if token name exists.
                token = GithubToken(client_key=client_key, token_name=token_name,
                                    token_value=jsonobject.get("access_token"))
                token.put()
            else:
                self.response.status = result.status_code
                return
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        self.redirect(str(config_url))


class GetGithubAuthTokens(webapp2.RequestHandler):
    def get(self):
        jwt = get_jwt_token(request=self.request)

        if not jwt:
            endpoints.UnauthorizedException("Authorization token not specified.")

        payload = validate_jwt_token(jwt)
        client_key = payload.get('iss')

        tokens = GithubToken.query(GithubToken.client_key == client_key)

        self.response.headers.add_header("Content-Type", "application/json")
        self.response.out.write(
            json.dumps([{'token_name': token.token_name, 'id': token.key.urlsafe()} for token in tokens]))


class DeleteAuthToken(webapp2.RequestHandler):
    def post(self):
        jwt = get_jwt_token(request=self.request)
        id = self.request.get('id')

        if not jwt:
            endpoints.UnauthorizedException("Authorization token not specified.")

        if not id:
            handle_404(self.response, "Requested token was not found.")
            return

        token_key = ndb.Key(urlsafe=id)
        token = token_key.get()
        if token is None:
            handle_404(self.response, "Token not found.")
            return

        payload = validate_jwt_token(jwt)
        client_key = payload.get('iss')

        if token.client_key != client_key:
            raise endpoints.UnauthorizedException("Token client key does not match account client key.")

        token_key.delete()
