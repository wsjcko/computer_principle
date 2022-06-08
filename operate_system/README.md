Python 的代码错误检查通常用 pep8、pylint和flake8，
自动格式化代码通常用 autopep8、yapf、black。这些工具均可以利用pip进行安装

settings.json
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "yapf",
    "python.linting.flake8Args": [
        "--max--line-length=248"
    ],
    "python.linting.pylintEnabled": false,
    "workbench.startupEditor": "newUntitledFile",
    // "python.pythonPath":"/usr/bin/python",
    "python.linting.enabled": true,