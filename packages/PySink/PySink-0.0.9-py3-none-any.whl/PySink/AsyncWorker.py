from PySide6.QtCore import QRunnable, Slot
from typing import Optional
import time
import uuid
from PySink.Objects import AsyncWorkerResults, AsyncWorkerSignals, AsyncWorkerProgress


class AsyncWorker(QRunnable):
    def __init__(self, identifier: Optional[str] = None, result_type=AsyncWorkerResults, signal_type=AsyncWorkerSignals):
        """A class that represents an Asynchronous Worker. Workers should inherit from this class
        and perform their long-running tasks by overriding the :meth:`~run` method..

        :param identifier: A unique identifier to differentiate this worker from other workers. Defaults to a uuid4 string
        :type identifier: str, optional
        :param result_type: The type that the results should be output in. Defaults to :class:`~AsyncWorkerResults`
        :type result_type: class, optional
        :param signal_type: The type of the :attr:`~signals` attribute. Defaults to :class:`~AsyncWorkerSignals`
        :type signal_type: class, optional
        """
        super(AsyncWorker, self).__init__()
        self.errors: list = []
        self.warnings: list = []
        self.id: str = identifier if identifier is not None else str(uuid.uuid4())
        self.signals: signal_type = signal_type()
        self.signal_type = signal_type
        self.results: result_type = result_type()
        self.result_type = result_type

    @Slot()
    def run(self) -> None:
        """Performs the worker's long-running task. Custom Workers should override this method. By default, this will
        perform a demo task of counting to 5 at a one-second interval.
        """
        self.emit_start()
        progress = 5
        self.update_progress(progress, 'Starting')
        for ii in range(5):
            time.sleep(1)
            progress += 90 / 5
            self.update_progress(progress, f'Step {ii+1}')
        self.complete(demo_result='Demo Result Value')

    def reset(self) -> None:
        """Resets the worker's state. All warnings and errors will be cleared, and :attr:`~result` will be reset to the
        defined result type.
        """
        self.errors = []
        self.warnings = []
        self.results = self.result_type()

    def update_progress(self, progress_value: int, message='') -> None:
        """Emits the progress value and message. These values are emitted via the
        :attr:`self.signals.progress<AsyncWorkerSignals.progress>` signal..

        :param progress_value: The current progress value. For discrete behavior, this value should be [0, 100].
            For indeterminate behavior, this value should be -1.
        :type progress_value: int
        :param message: A message describing the current progress stage of the worker ('Downloading', 'Calculating', etc).
        :type message: str, optional
        """
        progress = AsyncWorkerProgress()
        progress.value = progress_value
        progress.message = message
        progress.id = self.id
        self.signals.progress.emit(progress)

    def emit_start(self) -> None:
        """This method can be called within :meth:`~run` to let the application know that the long-running task has
        begun (this is signalled via the :attr:`self.signals.started<AsyncWorkerSignals.started>` signal). Calling
        this method is completely optional and does not affect the functionality of the worker.
        """
        self.signals.started.emit(self.id)

    def complete(self, **kwargs) -> None:
        """Signals the completion of the worker's long-running task. This should be called at the end of the overridden
        :meth:`~run` method. Calling this method emits the worker's results via the
        :attr:`self.signals.finished<AsyncWorkerSignals.finished>` signal.

        By default, the kwargs provided will be packaged into :attr:`results.results_dict<AsyncWorkerResults.results_dict>`
        as key-value pairs. However, if a custom result type was defined within :meth:`__init__()<AsyncWorker>`, the
        provided kwargs will be mapped to the attributes of the custom result type. In this scenario, the kwargs MUST
        match the defined attributes of the custom return type..

        :param kwargs: Result values to be emitted, defined as key-word arguments
        :raises AttributeError: If a custom return type is defined, the keys in kwargs MUST match the attributes of
            the return type, else an AttributeError will be raised.
        """
        self._load_default_results(clear=False)
        if self.result_type == AsyncWorkerResults:
            self.results.results_dict = kwargs
        else:
            for key in kwargs:
                getattr(self.results, key)
                setattr(self.results, key, kwargs[key])
        self.signals.finished.emit(self.results)

    def _load_default_results(self, clear=True) -> AsyncWorkerResults:
        if clear:
            self.results = self.result_type()
        self.results.errors = self.errors
        self.results.warnings = self.warnings
        self.results.id = self.id
        return self.results
