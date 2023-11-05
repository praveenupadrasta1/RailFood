from rest_framework.renderers import JSONRenderer

from BAAS.config import TOKEN_KEY, ERRORS_KEY, ROLE_KEY


class UserJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        charset = 'utf-8'
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        errors = data.get(ERRORS_KEY, None)

        data.pop(ROLE_KEY, None)

        # If we recieve a `token` key as art of the response, it will be a
        # byte object. Byte objects don't serialize well, so we need to
        # decode it before rendering the User object.
        token = data.get(TOKEN_KEY, None)

        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            # Also as mentioned above, we will decode `token` if it is of type
            # bytes
            data[TOKEN_KEY] = token.decode(charset)

        # Finally, we can render our data under the "user" namespace.
        return super(UserJSONRenderer, self).render(data)
