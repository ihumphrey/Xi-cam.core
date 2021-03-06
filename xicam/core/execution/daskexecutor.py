from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler
from dask.diagnostics import visualize
from xicam.core import msg
from appdirs import user_config_dir
import distributed


class DaskExecutor(object):
    def __init__(self):
        super(DaskExecutor, self).__init__()
        self.client = None

    def execute(self, wf, client=None):
        if not wf.processes:
            return {}

        if client is None:
            if self.client is None:
                self.client = distributed.Client()
            client = self.client

        dsk = wf.convertGraph()

        # with Profiler() as prof, ResourceProfiler(dt=0.25) as rprof, CacheProfiler() as cprof:
        result = client.get(dsk[0], dsk[1])

        msg.logMessage("result:", result, level=msg.DEBUG)
        # path = user_config_dir('xicam/profile.html')
        # visualize([prof, rprof, cprof], show=False, file_path=path)
        # msg.logMessage(f'Profile saved: {path}')

        wf.lastresult = result

        return result
