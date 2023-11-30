from multiprocessing import Process

from dashboard.engine.functions.process_functions import is_pid_alive, terminate_process


def test_is_pid_alive_and_terminate_process():
    class DummyProcess(Process):
        loop = True
        counter = 0

        def run(self):
            print(f"INSIDE PROCESS: {self.loop}")
            while self.loop:
                self.counter += 1
                print(self.counter)

    dummy_process = DummyProcess()

    dummy_process.start()
    datafeed_pid = dummy_process.pid

    if datafeed_pid is not None:
        # Check that the dummy process is alive
        assert is_pid_alive(datafeed_pid) is True

    # Terminate dummy process
    terminate_process(datafeed_pid)

    if datafeed_pid is not None:
        print(is_pid_alive(datafeed_pid))
    if datafeed_pid is not None:
        # Check that the dummy process is not alive
        assert is_pid_alive(datafeed_pid) is False
