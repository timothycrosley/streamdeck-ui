import fcntl
import os


class SemaphoreAcquireError(Exception):
    pass


class Semaphore:
    def __init__(self, semaphore_file):
        self.semaphore_file = semaphore_file
        self.semaphore_fd = None

    def __enter__(self):
        # create the semaphore file if it does not exist
        if not os.path.exists(self.semaphore_file):
            open(self.semaphore_file, "w").close()

        # open the file descriptor for the semaphore file
        self.semaphore_fd = os.open(self.semaphore_file, os.O_CREAT)

        try:
            fcntl.flock(self.semaphore_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise SemaphoreAcquireError("Could not acquire semaphore lock")

    def __exit__(self, exc_type, exc_value, traceback):
        # release the semaphore
        fcntl.flock(self.semaphore_fd, fcntl.LOCK_UN)

        # close the file descriptor
        os.close(self.semaphore_fd)

        # reset the file descriptor to None
        self.semaphore_fd = None
