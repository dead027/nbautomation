from typing import Any


def auto_repr(cls: Any) -> Any:
    """
    为类提供一个定制化的__repr__方法的类装饰器。
    这个方法包含实例的所有公共属性。

    参数:
    cls (Any): 要装饰的类。

    返回:
    Any: 带有修改过的__repr__方法的类。
    """

    def __repr__(self: Any) -> str:
        # 过滤私有属性并创建字符串表示。
        filtered_attrs = {k: v for k, v in vars(self).items() if not k.startswith('_')}
        attrs_str = ', '.join(f"{key}={value!r}" for key, value in filtered_attrs.items())
        return f"{self.__class__.__name__}({attrs_str})"

    # 为类设置自定义的__repr__方法。
    cls.__repr__ = __repr__
    return cls
