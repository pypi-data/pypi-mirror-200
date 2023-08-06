import httpx
from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
time = LazyLoader("time", globals())
warnings = LazyLoader("warnings", globals())
console = LazyLoader("console", globals(), "rich.console")
progress = LazyLoader("progress", globals(), "rich.progress")
utils = LazyLoader("utils", globals(), "pyxk.utils")


class Client(httpx.Client):
    """httpx.Client 重构

    pip install httpx
    """

    def __init__(self, headers=None, follow_redirects=True, **kwargs):
        headers = httpx.Headers(headers)
        headers.setdefault("user-agent", utils.UA_ANDROID)
        super().__init__(headers=headers, follow_redirects=follow_redirects, **kwargs)
        self.__console = console.Console()

    def send(self, request, **kwargs):
        exc_count, exc_max = {}, 10
        while True:
            try:
                with self.__console.status(f"[magenta b]Send Request[/]: {str(request.url)}"):
                    response = super().send(request, **kwargs)
                break
            # 请求超时
            except httpx.ConnectTimeout as exc:
                reason  = exc.args[0]
                timeout = request.extensions["timeout"]["connect"]
                warnings.warn(f"timeout: {timeout!r}", stacklevel=1)
                # except 计数
                exc_count.setdefault(reason, 0)
                exc_count[reason] += 1
                if exc_count[reason] >= exc_max:
                    raise
            # 无网络连接
            except httpx.ConnectError as exc:
                reason, reason_re = exc.args[0], ("[Errno 7]", )
                reason_ok = lambda : True in [reason.startswith(item) for item in reason_re]
                if not reason_ok():
                    raise
                warnings.warn("请检查网络连接是否正常...", stacklevel=1)
                time.sleep(1)
        return response

    def head(self, url, **kwargs):
        kwargs.setdefault("follow_redirects", False)
        return super().head(url=url, **kwargs)

    def wget(self, url, method="GET", *, output=None, resume=False, content=None, data=None, files=None, json=None, params=None, headers=None, cookies=None, auth=None, follow_redirects=True, timeout=5, extensions=None):
        """流媒体下载大文件

        :params: output: 下载文件路径
        :params: resume: 断点续传(default: False)
        """
        output = self.__set_wget_output(output, url, params=params, headers=headers, cookies=cookies, auth=auth, timeout=timeout, extensions=extensions)
        file_size, file_mode, chunk_size = 0, "wb", 1024
        # 开启文件续传
        if resume:
            if not output:
                warnings.warn("文件续传缺少 output")
            elif os.path.isfile(output):
                file_size, file_mode = os.path.getsize(output), "ab"
                headers = httpx.Headers(headers)
                headers["range"] = f"bytes={file_size}-"
        # 开启流式响应
        request  = self.build_request(method=method, url=url, content=content, data=data, files=files, json=json, params=params, headers=headers, cookies=cookies, timeout=timeout, extensions=extensions)
        response = self.send(request=request, auth=auth, follow_redirects=follow_redirects, stream=True)
        if not output:
            return response
        content_length = response.headers.get("Content-Length")
        if content_length is not None:
            content_length = int(content_length) + file_size
        with progress.Progress(
            *(
                # progress.SpinnerColumn("line"),
                progress.TextColumn("[progress.description]{task.description}"),
                progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                progress.BarColumn(finished_style="green"),
                progress.DownloadColumn(),
                # progress.TransferSpeedColumn(),
                progress.TimeElapsedColumn()
            ),
            console=self.__console, transient=True
        ) as download_progress:
            description = f"[bold]{os.path.basename(output)}[/]"
            download_task = download_progress.add_task(description=description, total=content_length)
            download_progress.update(download_task, advance=file_size)

            with utils.open(file=output, mode=file_mode) as file_obj:
                for chunk in response.iter_bytes(chunk_size):
                    file_obj.write(chunk)
                    download_progress.update(download_task, advance=chunk_size)
        return response

    def __set_wget_output(self, output, url, *, params=None, headers=None, cookies=None, auth=None, timeout=5, extensions=None):
        if not isinstance(output, str):
            return None
        output = os.path.normpath(os.path.abspath(output))
        if len(os.path.basename(output).rsplit(".", 1)) >= 2:
            return output
        response = self.head(url, params=params, headers=headers, cookies=cookies, auth=auth, timeout=timeout, extensions=extensions)
        content_type = response.headers.get("content-type")
        if not content_type:
            return None
        content_type = content_type.split(";", 1)[0].strip()
        content_type = content_type.rsplit("/", 1)[-1].strip()
        return output + "." + content_type if content_type else output
