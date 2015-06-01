import asyncio
from chaperone.cproc.subproc import SubProcess

class ForkingProcess(SubProcess):

    @asyncio.coroutine
    def process_started_co(self):
        yield from self.timed_wait(service.process_timeout, self._exit_timeout)
        
    def _exit_timeout(self):
        service = self.service
        message = "forking service '{1}' did not exit after {2} second(s), {3}".format(
            service.type,
            service.name, service.process_timeout, 
            "proceeding due to 'ignore_failures=True'" if service.ignore_failures else
            "terminating due to 'ignore_failures=False'")
        if not service.ignore_failures:
            self.terminate()
        raise Exception(message)