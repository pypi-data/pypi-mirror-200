# ddd-interface

定义跨库的数据结构

# 打包上传
```bash
rm -r dist

rm -r src/ddd_objects.egg-info

python3 -m pip install --upgrade setuptools wheel twine build

python3 -m build

python3 -m twine upload dist/*
```
# 下载使用
```bash
pip install ddd_interface
```
```python
import ddd_interface
```