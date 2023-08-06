from .folderawss3testcase import AWSS3ItemTestCase, AWSS3FolderTestCase
from heaserver.service.testcase.mixin import DeleteMixin, GetAllMixin, GetOneMixin, PutMixin, PostMixin, DeleteActivityMixin
from aiohttp import hdrs


class TestDeleteFolder(AWSS3FolderTestCase, DeleteMixin, DeleteActivityMixin):
    pass


class TestGetFolders(AWSS3FolderTestCase, GetAllMixin):
    async def test_options_status(self):
        """Checks if an OPTIONS request for all the folders succeeds with status 200."""
        obj = await self.client.request('OPTIONS',
                                        (self._href / '').path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_options(self):
        """
        Checks if the "Allow" header in a response to an OPTIONS request for all the folders contains GET, POST,
        HEAD, and OPTIONS and contains neither PUT nor DELETE.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / '').path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        if allow_hdr := obj.headers.get(hdrs.ALLOW):
            allow = {method.strip() for method in allow_hdr.split(',')}
        else:
            self.fail('No allow header')
        self.assertEqual({'GET', 'DELETE', 'HEAD', 'OPTIONS'}, allow)

    async def test_methods_not_allowed(self) -> None:
        """
        Checks if all the methods not in the "Allow" header in a response to an OPTIONS request for all the folders
        fail with status 405.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / '').path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        if allow_hdr := obj.headers.get(hdrs.ALLOW):
            allowed_methods = {method.strip() for method in allow_hdr.split(',')}
        else:
            self.fail('No allow header')
        all_methods = {'HEAD', 'OPTIONS', 'PUT', 'GET', 'DELETE'}
        prohibited_methods = all_methods - allowed_methods
        resps = {}
        for prohibited in prohibited_methods:
            obj = await self.client.request(prohibited,
                                            (self._href / '').path,
                                            headers=self._headers)
            resps |= {prohibited: obj.status}
        self.assertEqual(dict(zip(prohibited_methods, [405] * len(prohibited_methods))), resps)


class TestGetFolder(AWSS3FolderTestCase, GetOneMixin):
    async def test_options_status(self):
        """Checks if an OPTIONS request for a single folder succeeds with status 200."""
        obj = await self.client.request('OPTIONS',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_options(self):
        """
        Checks if the "Allow" header in a response to an OPTIONS request for a single folder contains GET, POST,
        HEAD, and OPTIONS and contains neither PUT nor DELETE.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        if allow_hdr := obj.headers.get(hdrs.ALLOW):
            allow = {method.strip() for method in allow_hdr.split(',')}
        else:
            self.fail('No allow header')
        self.assertEqual({'GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'}, allow)

    async def test_methods_not_allowed(self) -> None:
        """
        Checks if all the methods not in the "Allow" header in a response to an OPTIONS request for a single folder
        fail with status 405.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        if allow_hdr := obj.headers.get(hdrs.ALLOW):
            allowed_methods = {method.strip() for method in allow_hdr.split(',')}
        else:
            self.fail('No allow header')
        all_methods = {'HEAD', 'OPTIONS', 'POST', 'PUT', 'GET', 'DELETE'}
        prohibited_methods = all_methods - allowed_methods
        resps = {}
        for prohibited in prohibited_methods:
            obj = await self.client.request(prohibited,
                                            (self._href / self._id()).path,
                                            headers=self._headers)
            resps |= {prohibited: obj.status}
        self.assertEqual(dict(zip(prohibited_methods, [405] * len(prohibited_methods))), resps)


class TestDeleteItem(AWSS3ItemTestCase, DeleteMixin):
    pass


class TestGetItems(AWSS3ItemTestCase, GetAllMixin):
    async def test_options_status(self):
        """Checks if an OPTIONS request for all the folder items succeeds with status 200."""
        obj = await self.client.request('OPTIONS',
                                        (self._href / '').path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_options(self):
        """
        Checks if the "Allow" header in a response to an OPTIONS request for all the folder items contains GET, POST,
        HEAD, and OPTIONS and contains neither PUT nor DELETE.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / '').path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        if allow_hdr := obj.headers.get(hdrs.ALLOW):
            allow = {method.strip() for method in allow_hdr.split(',')}
        else:
            self.fail('No allow header')
        self.assertEqual({'GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'}, allow)

    async def test_methods_not_allowed(self) -> None:
        """
        Checks if all the methods not in the "Allow" header in a response to an OPTIONS request for all the folder
        items fail with status 405.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / '').path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        if allow_hdr := obj.headers.get(hdrs.ALLOW):
            allowed_methods = {method.strip() for method in allow_hdr.split(',')}
        else:
            self.fail('No allow header')
        all_methods = {'HEAD', 'OPTIONS', 'POST', 'PUT', 'GET', 'DELETE'}
        prohibited_methods = all_methods - allowed_methods
        resps = {}
        for prohibited in prohibited_methods:
            obj = await self.client.request(prohibited,
                                            (self._href / '').path,
                                            headers=self._headers)
            resps |= {prohibited: obj.status}
        self.assertEqual(dict(zip(prohibited_methods, [405] * len(prohibited_methods))), resps)


class TestGetItem(AWSS3ItemTestCase, GetOneMixin):
    async def test_options_status(self):
        """Checks if an OPTIONS request for a single folder item succeeds with status 200."""
        obj = await self.client.request('OPTIONS',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        self.assertEqual(200, obj.status)

    async def test_options(self):
        """
        Checks if the "Allow" header in a response to an OPTIONS request for a single folder item contains GET, POST,
        HEAD, and OPTIONS and contains neither PUT nor DELETE.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        if allow_hdr := obj.headers.get(hdrs.ALLOW):
            allow = {method.strip() for method in allow_hdr.split(',')}
        else:
            self.fail('No allow header')
        self.assertEqual({'GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'}, allow)

    async def test_methods_not_allowed(self) -> None:
        """
        Checks if all the methods not in the "Allow" header in a response to an OPTIONS request for a single folder item
        fail with status 405.
        """
        obj = await self.client.request('OPTIONS',
                                        (self._href / self._id()).path,
                                        headers=self._headers)
        if not obj.ok:
            self.fail(f'OPTIONS request failed: {await obj.text()}')
        if allow_hdr := obj.headers.get(hdrs.ALLOW):
            allowed_methods = {method.strip() for method in allow_hdr.split(',')}
        else:
            self.fail('No allow header')
        all_methods = {'HEAD', 'OPTIONS', 'POST', 'PUT', 'GET', 'DELETE'}
        prohibited_methods = all_methods - allowed_methods
        resps = {}
        for prohibited in prohibited_methods:
            obj = await self.client.request(prohibited,
                                            (self._href / self._id()).path,
                                            headers=self._headers)
            resps |= {prohibited: obj.status}
        self.assertEqual(dict(zip(prohibited_methods, [405] * len(prohibited_methods))), resps)

    async def test_get_by_name(self) -> None:
        self.skipTest('folder items do not support get by name')

    async def test_get_by_name_invalid_name(self):
        self.skipTest('GET by name not supported for AWS S3 folder items')


class TestPostItem(AWSS3ItemTestCase, PostMixin):
    pass


class TestPutItem(AWSS3ItemTestCase, PutMixin):
    pass
