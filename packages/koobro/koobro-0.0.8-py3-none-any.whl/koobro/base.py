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
        raise ValueError("总条数total_count必须>=0，每页数量per_page_count>0")
