Traceback (most recent call last):
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\connectionpool.py", line 464, in _make_request
    self._validate_conn(conn)
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\connectionpool.py", line 1093, in _validate_conn
    conn.connect()
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\connection.py", line 741, in connect
    sock_and_verified = _ssl_wrap_socket_and_match_hostname(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\connection.py", line 920, in _ssl_wrap_socket_and_match_hostname
    ssl_sock = ssl_wrap_socket(
               ^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\util\ssl_.py", line 460, in ssl_wrap_socket
    ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls, server_hostname)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\util\ssl_.py", line 504, in _ssl_wrap_socket_impl
    return ssl_context.wrap_socket(sock, server_hostname=server_hostname)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\SKSiltron\AppData\Local\Programs\Python\Python312\Lib\ssl.py", line 455, in wrap_socket
    return self.sslsocket_class._create(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\SKSiltron\AppData\Local\Programs\Python\Python312\Lib\ssl.py", line 1041, in _create
    self.do_handshake()
  File "C:\Users\SKSiltron\AppData\Local\Programs\Python\Python312\Lib\ssl.py", line 1319, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\connectionpool.py", line 787, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\connectionpool.py", line 488, in _make_request
    raise new_e
urllib3.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\requests\adapters.py", line 667, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\connectionpool.py", line 841, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\urllib3\util\retry.py", line 519, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='googlechromelabs.github.io', port=443): Max retries exceeded with url: /chrome-for-testing/latest-patch-versions-per-build.json (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\webdriver_manager\core\http.py", line 32, in get
    resp = requests.get(
           ^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\requests\api.py", line 73, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\requests\api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\requests\sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\requests\sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\requests\adapters.py", line 698, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: HTTPSConnectionPool(host='googlechromelabs.github.io', port=443): Max retries exceeded with url: /chrome-for-testing/latest-patch-versions-per-build.json (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)')))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\webdriver_manager\chrome.py", line 40, in install
    driver_path = self._get_driver_binary_path(self.driver)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\webdriver_manager\core\manager.py", line 35, in _get_driver_binary_path
    binary_path = self._cache_manager.find_driver(driver)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\webdriver_manager\core\driver_cache.py", line 107, in find_driver
    driver_version = self.get_cache_key_driver_version(driver)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\webdriver_manager\core\driver_cache.py", line 154, in get_cache_key_driver_version
    return driver.get_driver_version_to_download()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\webdriver_manager\core\driver.py", line 48, in get_driver_version_to_download
    return self.get_latest_release_version()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\webdriver_manager\drivers\chrome.py", line 59, in get_latest_release_version
    response = self._http_client.get(url)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\SKSiltron\Desktop\project\signpost_project\signpost_project_env\Lib\site-packages\webdriver_manager\core\http.py", line 35, in get
    raise exceptions.ConnectionError(f"Could not reach host. Are you offline?")
requests.exceptions.ConnectionError: Could not reach host. Are you offline?
