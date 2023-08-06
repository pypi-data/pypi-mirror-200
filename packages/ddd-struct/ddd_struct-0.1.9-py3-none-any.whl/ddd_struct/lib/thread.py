import asyncio, traceback, time
from functools import wraps, partial
from copy import copy



def async_wrap(func):
    if asyncio.iscoroutinefunction(func):
        return func
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run 


class CoroutinePool:
    def __init__(self, n_workers=10) -> None:
        self.n_workers = n_workers
        self.wait_list = []
        self.ret_list_when_timeout = None


    def _get_task_result(self, task):
        try:
            return task.result()
        except asyncio.CancelledError:
            return traceback.format_exc()
        except:
            pass
        try:
            return task.exception()
        except:
            return traceback.format_exc()


    def add_task(self, func, *args, **kwargs):
        self.wait_list.append((len(self.wait_list), func, args, kwargs))
   

    def execute(self, delay=0, timeout=100, n_workers=None):
        if n_workers is not None:
            self.n_workers = n_workers
        wait_list = copy(self.wait_list)

        async def run():
            start_time = time.time()
            ret_list = [None]*len(wait_list)
            runner = []
            
            for _ in range(1000000000):
                if (time.time()-start_time)>timeout:
                    self.ret_list_when_timeout = ret_list
                    raise ValueError(f'Fail to finish task in {timeout}s')

                # create task
                if len(runner)<self.n_workers and wait_list:
                    idx, func, args, kwargs = wait_list.pop()
                    func = async_wrap(func)
                    task = asyncio.create_task(func(*args, **kwargs))
                    runner.append((idx, task))
                else:
                    # check tasks
                    for i, (idx, task) in enumerate(runner):
                        if not task.done():
                            continue
                        ret_list[idx] = self._get_task_result(task)
                        runner[i] = None
                    runner = [r for r in runner if r]

                    #exit
                    if not runner and not wait_list:
                        break
                    await asyncio.sleep(delay)
            return ret_list

        event_loop = asyncio.get_event_loop()
        ret_list = event_loop.run_until_complete(run())
        # ret_list = asyncio.run(run())
        self.wait_list = []
        return ret_list
                


