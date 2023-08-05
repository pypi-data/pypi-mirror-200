import json

import responses

from superwise import Client
from superwise import Config


@responses.activate
def test_token_refresh():
    def request_callback_generator():
        # payload = json.loads(request.body)
        return_403 = True

        def _callback(request):
            nonlocal return_403
            valid_resp_body = {
                "expires": "Thu, 29 Sep 2022 08:00:41 GMT",
                "expiresIn": 86400,
                "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlkYmRlNzNkIn0.eyJzdWIiOiI0NGE4ODc3YS0yOWJhLTQ2NTYtOGY1OC1lMTQzYTM4MTQ5MTMiLCJlbWFpbCI6InN3X3Rlc3RzQHN1cGVyd2lzZS5haSIsInVzZXJNZXRhZGF0YSI6eyJvbmJvYXJkaW5nIjp0cnVlfSwidGVuYW50SWQiOiJ0ZXN0cyIsInJvbGVzIjpbIlVzZXIiXSwicGVybWlzc2lvbnMiOlsiZmUuc2VjdXJlLndyaXRlLnVzZXJBcGlUb2tlbnMiLCJmZS5zZWN1cmUuZGVsZXRlLnVzZXJBcGlUb2tlbnMiLCJmZS5zZWN1cmUucmVhZC51c2VyQXBpVG9rZW5zIiwiZmUuc2VjdXJlLnJlYWQudGVuYW50QXBpVG9rZW5zIl0sIm1ldGFkYXRhIjp7fSwiY3JlYXRlZEJ5VXNlcklkIjoiZTAyNGE1ZTItNzZkMS00N2YyLWE2NWUtMDViMTFjNzI2MDZlIiwidHlwZSI6InVzZXJBcGlUb2tlbiIsInVzZXJJZCI6ImUwMjRhNWUyLTc2ZDEtNDdmMi1hNjVlLTA1YjExYzcyNjA2ZSIsImF1ZCI6IjlkYmRlNzNkLWViODktNGMxMC05ZDY1LTYwNTI1ZGE0ZDlkNiIsImlzcyI6ImZyb250ZWdnIiwiaWF0IjoxNjY0MzUyMDQxLCJleHAiOjE2NjQ0Mzg0NDF9.UWEqljuU1txF5VDVIqJO8zDY10myPuYqIwx72ClriJh4fAW84jypeDoopVfD01kKHeZDGwJ9YmlGmc6rwQij7YPjXvMRlBSWdshz-2qM7rhY8IOuSBUsW-GgS9BUTKL14K1vbpZ6rLpTEJNoeAoIUKxztynbXhAZVEci78Q_bM29Bs-urSHrzy_hu0hrzAjDKyNkHkNB0DYLiqf03SzyuJDNlj-fvcXp0EaIeqT1FOcpSeJqPgJ57JXrsxg8o_IwZsN-AR_aGdb-zyw0hVwJCzF1wNWMUROo-o2yFBVBwlbh4PMBQkkTA0hiNNqMPI7rA45c2NVicok_e0bi6ZlYkA",
                "refreshToken": "26323edd-8551-422b-99b6-353c76139359",
            }
            headers = {}
            if return_403:
                return_403 = False
                return (403, headers, json.dumps({}))
            return (200, headers, json.dumps(valid_resp_body))

        return _callback

    responses.post(
        "https://auth.superwise.ai/identity/resources/auth/v1/api-token",
        status=200,
        json={
            "expires": "Thu, 29 Sep 2022 08:00:41 GMT",
            "expiresIn": 86400,
            "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlkYmRlNzNkIn0.eyJzdWIiOiI0NGE4ODc3YS0yOWJhLTQ2NTYtOGY1OC1lMTQzYTM4MTQ5MTMiLCJlbWFpbCI6InN3X3Rlc3RzQHN1cGVyd2lzZS5haSIsInVzZXJNZXRhZGF0YSI6eyJvbmJvYXJkaW5nIjp0cnVlfSwidGVuYW50SWQiOiJ0ZXN0cyIsInJvbGVzIjpbIlVzZXIiXSwicGVybWlzc2lvbnMiOlsiZmUuc2VjdXJlLndyaXRlLnVzZXJBcGlUb2tlbnMiLCJmZS5zZWN1cmUuZGVsZXRlLnVzZXJBcGlUb2tlbnMiLCJmZS5zZWN1cmUucmVhZC51c2VyQXBpVG9rZW5zIiwiZmUuc2VjdXJlLnJlYWQudGVuYW50QXBpVG9rZW5zIl0sIm1ldGFkYXRhIjp7fSwiY3JlYXRlZEJ5VXNlcklkIjoiZTAyNGE1ZTItNzZkMS00N2YyLWE2NWUtMDViMTFjNzI2MDZlIiwidHlwZSI6InVzZXJBcGlUb2tlbiIsInVzZXJJZCI6ImUwMjRhNWUyLTc2ZDEtNDdmMi1hNjVlLTA1YjExYzcyNjA2ZSIsImF1ZCI6IjlkYmRlNzNkLWViODktNGMxMC05ZDY1LTYwNTI1ZGE0ZDlkNiIsImlzcyI6ImZyb250ZWdnIiwiaWF0IjoxNjY0MzUyMDQxLCJleHAiOjE2NjQ0Mzg0NDF9.UWEqljuU1txF5VDVIqJO8zDY10myPuYqIwx72ClriJh4fAW84jypeDoopVfD01kKHeZDGwJ9YmlGmc6rwQij7YPjXvMRlBSWdshz-2qM7rhY8IOuSBUsW-GgS9BUTKL14K1vbpZ6rLpTEJNoeAoIUKxztynbXhAZVEci78Q_bM29Bs-urSHrzy_hu0hrzAjDKyNkHkNB0DYLiqf03SzyuJDNlj-fvcXp0EaIeqT1FOcpSeJqPgJ57JXrsxg8o_IwZsN-AR_aGdb-zyw0hVwJCzF1wNWMUROo-o2yFBVBwlbh4PMBQkkTA0hiNNqMPI7rA45c2NVicok_e0bi6ZlYkA",
            "refreshToken": "26323edd-8551-422b-99b6-353c76139359",
        },
    )
    responses.add_callback(
        responses.POST,
        "https://https//something.com/tests//something",
        callback=request_callback_generator(),
        content_type="application/json",
    )
    # with responses.RequestsMock() as rsps:
    client = Client(None, "secret", "https://something.com")
    client.post(client.build_url("/something"), params={})
