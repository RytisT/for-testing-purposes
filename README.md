`` not style

 use
 ``` 
code
 ``` 
no style by default,have to 

```JSON 
{
    "key": "mohamicorp-render-markdownn",
    "name": "Markdown Extensions for Confluence",
    "description": "Provide macro for displaying markdown content in Confluence pages.",
    "baseUrl": "https://4fbcf35c.ngrok.io",
    "enableLicensing": true,
    "vendor": {
        "name": "Mohami",
        "url": "http://mohami.io"
    },
    "authentication": {
        "type": "jwt"
    },
    "apiMigrations": {
        "gdpr": true
    },
    "lifecycle": {
        "installed": "/markdown_installed"
    },
    "version": "1.3.0-AC",
    "modules": {
        "dynamicContentMacros": [
            {
                "url": "/display.html?pageId={page.id}&pageVersion={page.version}&macroHash={macro.hash}&macroId={macro.id}&outputType={output.type}",
                "description": {
                    "i18n": "markdown.macro.desc",
                    "value": "Allows inserting and viewing markdown in confluence pages."
                },
                "renderModes": {
                    "default": {
                        "url": "/get_markdown_macro_id?pageId={page.id}&pageVersion={page.version}&macroHash={macro.hash}&macroId={macro.id}"
                    }
                },
                "icon": {
                    "width": 80,
                    "height": 76,
                    "url": "/images/macro-icon.png"
                },
                "documentation": {
                    "url": "https://mohamicorp.atlassian.net/wiki/spaces/DOC/pages/3407891/Markdown+Extensions+for+Confluence"
                },
                "categories": [
                    "formatting", "confluence-content"
                ],
                "outputType": "block",
                "bodyType": "plain-text",
                "key": "mohamicorp-markdown",
                "name": {
                    "value": "Markdown"
                },
                "editor": {
                    "url": "/editor.html",
                    "width": "865px",
                    "height": "493px"
                }
            },
            {
                "url": "/display-url.html?url={url}",
                "renderModes": {
                    "default": {
                        "url": "/get_markdown_static?url={url}"
                    }
                },
                "description": {
                    "i18n": "markdown.macro.url.desc",
                    "value": "This macro grabs markdown from a url and renders it into HTML."
                },
                "icon": {
                    "width": 80,
                    "height": 76,
                    "url": "/images/macro-icon.png"
                },
                "documentation": {
                    "url": "https://mohamicorp.atlassian.net/wiki/spaces/DOC/pages/3407891/Markdown+Extensions+for+Confluence"
                },
                "categories": [
                    "confluence-content", "formatting"
                ],
                "outputType": "block",
                "bodyType": "none",
                "key": "mohamicorp-markdown-url",
                "name": {
                    "value": "Markdown from a URL"
                },
                "parameters": [
                    {
                        "identifier": "url",
                        "name": {
                            "value": "URL"
                        },
                        "description": {
                            "value": "Enter the URL for your Markdown"
                        },
                        "type": "string",
                        "required": true
                    },
                    {
                        "identifier": "string",
                        "name": {
                            "value": "Personal Authentication Token"
                        },
                        "description": {
                            "value": "Enter the Personal Authentication Token from Github"
                        },
                        "type": "string",
                        "hidden": true
                    }
                ],
                "autoconvert": {
                    "urlParameter": "url",
                    "matchers": [
                        {
                            "pattern": "http://{}"
                        },
                        {
                            "pattern": "https://{}"
                        }
                    ]
                }
            },
            {
                "url": "/client/display-url-github.html?url={url}&token={token}",
                "renderModes": {
                    "default": {
                        "url": "/get_markdown_static?url={url}&token={token}"
                    }
                },
                "description": {
                    "i18n": "markdown.macro.github.desc",
                    "value": "Insert markdown from private Github Repositories."
                },
                "icon": {
                    "width": 80,
                    "height": 76,
                    "url": "/images/macro-icon.png"
                },
                "documentation": {
                    "url": "https://mohamicorp.atlassian.net/wiki/spaces/DOC/pages/3407891/Markdown+Extensions+for+Confluence"
                },
                "categories": [
                    "formatting", "confluence-content"
                ],
                "outputType": "block",
                "bodyType": "none",
                "key": "mohamicorp-markdown-github",
                "name": {
                    "value": "Markdown from Github"
                },
                "editor": {
                    "url": "/client/github-token-selector.html",
                    "width": "865px",
                    "height": "493px"
                }
            },
            {
                "url": "/client/display-url-bitbucket.html?url={url}&user={user}&repo={repo}&branch={branch}&path={path}&token={token}",
                "renderModes": {
                    "default": {
                        "url": "/get_bitbucket_markdown?url={url}&user={user}&repo={repo}&branch={branch}&path={path}&token={token}"
                    }
                },
                "description": {
                    "i18n": "markdown.macro.github.desc",
                    "value": "Insert markdown from private Bitbucket Repositories."
                },
                "icon": {
                    "width": 80,
                    "height": 76,
                    "url": "/images/macro-icon.png"
                },
                "documentation": {
                    "url": "https://mohamicorp.atlassian.net/wiki/spaces/DOC/pages/3407891/Markdown+Extensions+for+Confluence"
                },
                "categories": [
                    "formatting", "confluence-content"
                ],
                "outputType": "block",
                "bodyType": "none",
                "key": "mohamicorp-markdown-bitbucket",
                "name": {
                    "value": "Markdown from Bitbucket"
                },
                "editor": {
                    "url": "/client/bitbucket-token-selector.html",
                    "width": "865px",
                    "height": "493px"
                }
            }
        ],
        "adminPages": [
            {
                "url": "/client/configuration-editor.html",
                "key": "markdown-macro-admin-page",
                "name": {
                    "value": "Markdown Extensions Configuration"
                }
            }
        ],
        "configurePage": {
            "url": "/client/configuration-editor.html",
            "key": "markdown-macro-configure",
            "name": {
                "value": "Markdown Extensions Configuration"
            }
        }
    },
    "scopes": [
        "read"
    ]
}

 ```
