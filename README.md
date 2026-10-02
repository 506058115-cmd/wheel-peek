# wheel-peek

静态读取 Python wheel 的名称、版本、Python 版本要求、兼容标签和依赖声明。不会安装 wheel，也不会执行其中的代码。

## 使用

需要 Python 3.8+，不安装依赖。

~~~sh
python wheel_peek.py ./dist/example-1.2.3-py3-none-any.whl
~~~

工具仅读取 ZIP 容器中的 `.dist-info/METADATA` 与可选 `WHEEL` 文件，并将元数据限制为 1 MiB。它不会验证签名、审计源码、安装依赖或证明软件安全；依赖声明仅供查看。

退出状态：0 表示元数据已读取，2 表示归档或元数据无效，130 表示中断。

## 许可

MIT，见 [LICENSE](LICENSE)。

## Linux x86_64 下载

- [单文件版](https://github.com/506058115-cmd/wheel-peek/releases/download/v1.0.0/wheel-peek-linux-x86_64-onefile.tar.gz)
- [目录版](https://github.com/506058115-cmd/wheel-peek/releases/download/v1.0.0/wheel-peek-linux-x86_64-onedir.tar.gz)
- [v1.0.0 Release 页面](https://github.com/506058115-cmd/wheel-peek/releases/tag/v1.0.0)

压缩包附带构建信息和依赖许可证；Release 另附 SHA-256 校验文件。构建目标为 GNU/Linux x86_64。较旧发行版可能需要兼容的 glibc。
