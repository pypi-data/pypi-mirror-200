import re


def cal_page_count(total_count: int, per_page_count: int) -> int:
    """
    根据总条数和每页数量计算页数

    Args:
        total_count: 总条数
        per_page_count: 每页数量

    Returns:
        总页数
    """

    if total_count >= 0 and per_page_count > 0:
        if total_count == 0:
            return 1
        else:
            return total_count // per_page_count if total_count % per_page_count == 0 else total_count // per_page_count + 1
    else:
        raise ValueError("总条数total_count必须>=0，每页数量per_page_count必须>0")


def has_invalid_windows_chars(string: str) -> bool:
    """
    检测windows下，字符串是否包含非法字符
        - <>:"/\|?*：这些字符在Windows中被视为非法字符。
        - \x00-\x1f：这些字符是ASCII控制字符，也被视为非法字符。

    Args:
        string: 需要检测的字符串

    Returns:
        检测结果：包含为True，不包含为False
    """

    pattern = r'[<>:"/\\|?*\x00-\x1f]'
    return bool(re.search(pattern, string))


if __name__ == '__main__':
    print(cal_page_count(11, 5))
    print(has_invalid_windows_chars("gg*geg"))
