import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logkk",  # 模块名称
    version="0.4.0",  # 当前版本
    author="olivetree",  # 作者
    author_email="olivetree123@163.com",  # 作者邮箱
    description="日志组件",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    url="https://github.com/olivetree/logkk",  # 模块github地址
    packages=["logkk"],  # 自动找到项目中导入的模块
    # 模块相关的元数据（更多的描述）
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[],
    # python版本
    python_requires=">=3.7",
)
