from pyzero_dtq_client.application import Application


class AppStub(Application):
    '''A application stub that the client will use for testing purposes
    '''

    def __init__(self):
        self.run_once = False
        self.results = []

    def get_task(self):
        '''Return a task only the first time
        '''
        if not self.run_once:
            task = [x for x in range(10)]
            self.run_once = True
            return task
        return False

    def add_result(self, result):
        self.results.append(result)

    def get_results(self):
        return self.results

    def done(self):
        '''The AppStub will be done with the tasks after having run once.
        '''
        return len(self.results) > 0
