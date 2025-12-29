import concurrent.futures
from typing import Callable, Iterable, Any, List, Optional
import time
import threading
from functools import wraps
from functools import partial

def timeout_decorator(timeout):
    """装饰器：为函数添加超时限制"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result_container = []
            exception_container = []
            
            def worker():
                try:
                    result_container.append(func(*args, **kwargs))
                except Exception as e:
                    exception_container.append(e)
            
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            thread.join(timeout)
            
            if thread.is_alive():
                # 线程仍在运行，表示超时
                raise TimeoutError(f"Function {func.__name__} timed out after {timeout} seconds")
            
            if exception_container:
                raise exception_container[0]
            
            return result_container[0]
        return wrapper
    return decorator

class ConcurrentMap:
    """
    并发版本的map函数实现，支持额外参数
    """
    
    @staticmethod
    def thread_map(func: Callable, iterable: Iterable, *args, max_workers: int = None, 
                   timeout: float = None, **kwargs) -> List[Any]:
        """
        使用线程池实现的map，支持额外参数
        
        Args:
            func: 要执行的函数
            iterable: 可迭代对象
            *args: 传递给函数的额外位置参数
            max_workers: 最大工作线程数，默认使用cpu_count() * 5
            timeout: 超时时间（秒）
            **kwargs: 传递给函数的额外关键字参数
        
        Returns:
            处理结果列表
        """
        import os
        if max_workers is None:
            max_workers = min(32, (os.cpu_count() or 1) * 5)
        
        # 使用partial固定额外参数
        if args or kwargs:
            func = partial(func, *args, **kwargs)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            if timeout:
                timed_func = timeout_decorator(timeout)(func)
                futures = {executor.submit(func, item): item for item in iterable}
                results = []
                for future in concurrent.futures.as_completed(futures, timeout=timeout):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append(e)
                return results
            else:
                return list(executor.map(func, iterable))
    
    @staticmethod
    def process_map(func: Callable, iterable: Iterable, *args, max_workers: int = None, 
                    timeout: float = None, chunksize: int = 1, **kwargs) -> List[Any]:
        """
        使用进程池实现的map（适合CPU密集型任务），支持额外参数
        
        Args:
            func: 要执行的函数
            iterable: 可迭代对象
            *args: 传递给函数的额外位置参数
            max_workers: 最大工作进程数，默认使用cpu_count()
            timeout: 超时时间（秒）
            chunksize: 分块大小，提高大任务性能
            **kwargs: 传递给函数的额外关键字参数
        
        Returns:
            处理结果列表
        """
        import os
        if max_workers is None:
            max_workers = os.cpu_count() or 1
        
        # 使用partial固定额外参数
        if args or kwargs:
            func = partial(func, *args, **kwargs)
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            if timeout:
                futures = {executor.submit(func, item): item for item in iterable}
                results = []
                for future in concurrent.futures.as_completed(futures, timeout=timeout):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append(e)
                return results
            else:
                # 使用chunksize提高大任务性能
                return list(executor.map(func, iterable, chunksize=chunksize))
    
    @staticmethod
    def async_map(func: Callable, iterable: Iterable, *args, max_workers: int = None, 
                  timeout: float = None, chunksize: int = 1, 
                  cpu_intensive: Optional[bool] = None, **kwargs) -> List[Any]:
        """
        优化的map实现，自动根据任务类型选择执行方式，支持额外参数
        
        Args:
            func: 要执行的函数
            iterable: 可迭代对象
            *args: 传递给函数的额外位置参数
            max_workers: 最大工作线程/进程数
            timeout: 超时时间（秒）
            chunksize: 分块大小，用于ProcessPoolExecutor提高性能
            cpu_intensive: 手动指定是否是CPU密集型任务，None表示自动判断
            **kwargs: 传递给函数的额外关键字参数
        
        Returns:
            处理结果列表
        """
        # 判断是否是CPU密集型任务
        if cpu_intensive is None:
            cpu_intensive = ConcurrentMap._is_cpu_intensive(func)
        
        if cpu_intensive:
            return ConcurrentMap.process_map(
                func, iterable, *args, 
                max_workers=max_workers, 
                timeout=timeout, 
                chunksize=chunksize, 
                **kwargs
            )
        else:
            return ConcurrentMap.thread_map(
                func, iterable, *args, 
                max_workers=max_workers, 
                timeout=timeout, 
                **kwargs
            )
    
    @staticmethod
    def _is_cpu_intensive(func: Callable) -> bool:
        """
        简单判断函数是否是CPU密集型
        
        这里可以扩展更复杂的判断逻辑
        """
        # 简单的启发式判断
        func_name = func.__name__.lower()
        
        # 一些可能表示CPU密集型的函数名关键词
        cpu_keywords = {
            'compute', 'calculate', 'process', 'analyze', 'simulate',
            'train', 'fit', 'predict', 'transform', 'encode', 'decode'
        }
        
        # 检查函数名是否包含CPU密集型关键词
        for keyword in cpu_keywords:
            if keyword in func_name:
                return True
        
        # 默认判断为I/O密集型，使用线程池
        # 用户可以通过cpu_intensive参数手动指定
        return False
