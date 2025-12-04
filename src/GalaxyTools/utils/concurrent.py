from typing import Callable, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def run_concurrently(
    func: Callable,
    args_list: List[tuple],
    kwargs_list: List[dict] = None,
    max_workers: int = None,
    use_threads: bool = True
) -> List[Any]:
    """
    并发执行函数 func，对 args_list 中的每组参数调用一次 func。

    参数:
        func (Callable): 要并发执行的函数。
        args_list (List[tuple]): 每个元素是一个元组，表示传递给 func 的位置参数。
        kwargs_list (List[dict]):每个元素是一个词典，表示传递给 func 的非关键参数参数。
        max_workers (int, optional): 最大并发线程/进程数。默认为 None（由系统决定）。
        use_threads (bool): 若为 True 使用线程池（适合 I/O 密集型），
                            若为 False 使用进程池（适合 CPU 密集型）。

    返回:
        List[Any]: 与 args_list 顺序一致的结果列表。
    """

    Executor = ThreadPoolExecutor if use_threads else ProcessPoolExecutor
    results = [None] * len(args_list)
    with Executor(max_workers=max_workers) as executor:
        # 提交所有任务并保留 future 到原始索引的映射
        future_to_index = {
            executor.submit(func, *args,**kwargs): i
            for i, (args, kwargs) in enumerate(zip(args_list, kwargs_list))
        }

        # 按完成顺序收集结果（但最终按原始顺序返回）
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                results[index] = future.result()
            except Exception as exc:
                # 可根据需要自定义异常处理，这里简单抛出或记录
                raise RuntimeError(f"Task {index} generated an exception: {exc}") from exc
    return results