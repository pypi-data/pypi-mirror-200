A general purpose Task and TaskQueue for running tasks with
dependencies and failure/retry, potentially in parallel.

*Latest release 20230401*:
Add missing requirement to DISTINFO.

## Class `BaseTask(cs.fsm.FSM, cs.gvutils.DOTNodeMixin, cs.resources.RunStateMixin)`

A base class subclassing `cs.fsm.FSM` with a `RunStateMixin`.

Note that this class and the `FSM` base class does not provide
a `FSM_DEFAULT_STATE` attribute; a default `state` value of
`None` will leave `.fsm_state` _unset_.

This behaviour is is chosen mostly to support subclasses
with unusual behaviour, particularly Django's `Model` class
whose `refresh_from_db` method seems to not refresh fields
which already exist, and setting `.fsm_state` from a
`FSM_DEFAULT_STATE` class attribute thus breaks this method.
Subclasses of this class and `Model` should _not_ provide a
`FSM_DEFAULT_STATE` attribute, instead relying on the field
definition to provide this default in the usual way.

*Method `BaseTask.as_dot(self, name=None, **kw)`*:
Return a DOT syntax digraph starting at this `Task`.
Parameters are as for `Task.tasks_as_dot`.

*Method `BaseTask.dot_node_label(self)`*:
The default DOT node label.

*Method `BaseTask.tasks_as_dot(tasks, name=None, *, follow_blocking=False, sep=None)`*:
Return a DOT syntax digraph of the iterable `tasks`.
        Nodes will be coloured according to `DOT_NODE_FILLCOLOR_PALETTE`
        based on their state.

        Parameters:
        * `tasks`: an iterable of `Task`s to populate the graph
        * `name`: optional graph name
        * `follow_blocking`: optional flag to follow each `Task`'s
          `.blocking` attribute recursively and also render those
          `Task`s
        * `sep`: optional node seprator, default `'
'`

*Method `BaseTask.tasks_as_svg(tasks, name=None, **kw)`*:
Return an SVG diagram of the iterable `tasks`.
This takes the same parameters as `tasks_as_dot`.

## Class `BlockedError(TaskError, cs.fsm.FSMError, builtins.Exception, builtins.BaseException)`

Raised by a blocked `Task` if attempted.

## Function `main(argv)`

Dummy main programme to exercise something.

## Function `make(*tasks, fail_fast=False, queue=None)`

Generator which completes all the supplied `tasks` by dispatching them
once they are no longer blocked.
Yield each task from `tasks` as it completes (or becomes cancelled).

Parameters:
* `tasks`: `Task`s as positional parameters
* `fail_fast`: default `False`; if true, cease evaluation as soon as a
  task completes in a state with is not `DONE`
* `queue`: optional callable to submit a task for execution later
  via some queue such as `Later` or celery

The following rules are applied by this function:
- if a task is being prepared, raise an `FSMError`
- if a task is already running or queued, wait for its completion
- if a task is pending:
  * if any prerequisite has failed, fail this task
  * if any prerequisite is cancelled, cancel this task
  * if any prerequisite is pending, make it first
  * if any prerequisite is not done, fail this task
  * otherwise dispatch this task and then yield it
- if `fail_fast` and the task is not done, return

Examples:

    >>> t1 = Task('t1', lambda: print('doing t1'), track=True)
    >>> t2 = t1.then('t2', lambda: print('doing t2'), track=True)
    >>> list(make(t2))    # doctest: +ELLIPSIS
    t1 PENDING->dispatch->RUNNING
    doing t1
    t1 RUNNING->done->DONE
    t2 PENDING->dispatch->RUNNING
    doing t2
    t2 RUNNING->done->DONE
    [Task('t2',<function <lambda> at ...>,state='DONE')]

## Function `make_later(L, *tasks, fail_fast=False)`

Dispatch the `tasks` via `L:Later` for asynchronous execution
if it is not already completed.
The caller can wait on `t.result` for completion.

This calls `make_now()` in a thread and uses `L.defer` to
queue the task and its prerequisites for execution.

## Function `make_now(*tasks, fail_fast=False, queue=None)`

Run the generator `make(*tasks)` to completion and return the
list of completed tasks.

## Class `Task(BaseTask, cs.fsm.FSM, cs.gvutils.DOTNodeMixin, cs.resources.RunStateMixin, cs.threads.HasThreadState, cs.context.ContextManagerMixin)`

A task which may require the completion of other tasks.

The model here may not be quite as expected; it is aimed at
tasks which can be repaired and rerun.
As such, if `self.run(func,...)` raises an exception from
`func` then this `Task` will still block dependent `Task`s.
Dually, a `Task` which completes without an exception is
considered complete and does not block dependent `Task`s.

Keyword parameters:
* `cancel_on_exception`: if true, cancel this `Task` if `.run`
  raises an exception; the default is `False`, allowing repair
  and retry
* `cancel_on_result`: optional callable to test the `Task.result`
  after `.run`; if the callable returns `True` the `Task` is marked
  as cancelled, allowing repair and retry
* `func`: the function to call to complete the `Task`;
  it will be called as `func(*func_args,**func_kwargs)`
* `func_args`: optional positional arguments, default `()`
* `func_kwargs`: optional keyword arguments, default `{}`
* `lock`: optional lock, default an `RLock`
* `state`: initial state, default from `self._state.initial_state`,
  which is initally '`PENDING`'
* `track`: default `False`;
  if `True` then apply a callback for all states to print task transitions;
  otherwise it should be a callback function suitable for `FSM.fsm_callback`
Other arguments are passed to the `Result` initialiser.

Example:

    t1 = Task(name="task1")
    t1.bg(time.sleep, 10)
    t2 = Task(name="task2")
    # prevent t2 from running until t1 completes
    t2.require(t1)
    # try to run sleep(5) for t2 immediately after t1 completes
    t1.notify(t2.call, sleep, 5)

Users wanting more immediate semantics can supply
`cancel_on_exception` and/or `cancel_on_result` to control
these behaviours.

Example:

    t1 = Task(name="task1")
    t1.bg(time.sleep, 2)
    t2 = Task(name="task2")
    # prevent t2 from running until t1 completes
    t2.require(t1)
    # try to run sleep(5) for t2 immediately after t1 completes
    t1.notify(t2.call, sleep, 5)

*Method `Task.__call__(self)`*:
Block on `self.result` awaiting completion
by calling `self.result()`.

*Method `Task.bg(self)`*:
Dispatch a function to complete the `Task` in a separate `Thread`,
returning the `Thread`.
This raises `BlockedError` for a blocked task.
otherwise the thread runs `self.dispatch()`.

*Method `Task.block(self, otask)`*:
Block another task until we are complete.
The converse of `.require()`.

*Method `Task.blockers(self)`*:
A generator yielding tasks from `self.required`
which should block this task.
Aborted tasks are not blockers
but if we encounter one we do abort the current task.

*Method `Task.cancel(self)`*:
Transition this `Task` to `CANCELLED` state.
If the task is running, set `.cancelled` on the `RunState`,
allowing clean task cancellation and subsequent transition
(mediated by the `.run()` method).
Otherwise fire the `'cancel'` event directly.

*Method `Task.dispatch(self)`*:
Dispatch the `Task`:
If the task is blocked, raise `BlockedError`.
If a prerequisite is aborted, fire the 'abort' method.
Otherwise fire the `'dispatch'` event and then run the
task's function via the `.run()` method.

*Method `Task.isblocked(self)`*:
A task is blocked if any prerequisite is not complete.

*Method `Task.iscompleted(self)`*:
This task is completed (even if failed) and does not block contingent tasks.

*Method `Task.join(self)`*:
Wait for this task to complete.

*Method `Task.make(self, fail_fast=False)`*:
Complete `self` and its prerequisites.
This calls the global `make()` function with `self`.
It returns a Boolean indicating whether this task completed.

*`Task.perthread_state`*

*Method `Task.require(self, otask: 'TaskSubType')`*:
Add a requirement that `otask` be complete before we proceed.
This is the simple `Task` only version of `.then()`.

*Method `Task.run(self)`*:
Run the function associated with this task,
completing the `self.result` `Result` appropriately when finished.

*WARNING*: this _ignores_ the current state and any blocking `Task`s.
You should usually use `dispatch` or `make`.

During the run the thread local `Task.default()`
will be `self` and the `self.runstate` will be running.

Otherwise run `func_result=self.func(*self.func_args,**self.func_kwargs)`
with the following effects:
* if the function raises a `CancellationError`, cancel the `Task`
* if the function raises another exception,
  if `self.cancel_on_exception` then cancel the task
  else complete `self.result` with the exception
  and fire the `'error'` `event
* if `self.runstate.canceled` or `self.cancel_on_result`
  was provided and `self.cancel_on_result(func_result)` is
  true, cancel the task
* otherwise complete `self.result` with `func_result`
  and fire the `'done'` event

*Method `Task.then(self, func: Union[str, Callable, ForwardRef('TaskSubType')], *a, func_args=(), func_kwargs=None, **task_kw)`*:
Prepare a new `Task` or function which may not run before `self` completes.
This may be called in two ways:
- `task.then(some_Task): block the `Task` instance `some_Task` behind `self`
- `task.then([name,]func[,func_args=][,func_kwargs=][,Task_kwargs...]):
  make a new `Task` to be blocked behind `self`
Return the new `Task`.

This supports preparing a chain of actions:

    >>> t_root = Task("t_root", lambda: 0)
    >>> t_leaf = t_root.then(lambda: 1).then(lambda: 2)
    >>> t_root.iscompleted()   # the root task has not yet run
    False
    >>> t_leaf.iscompleted()   # the final task has not yet run
    False
    >>> # t_leaf is blocked by t_root
    >>> t_leaf.dispatch()      # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    cs.taskqueue.BlockedError: ...
    >>> t_leaf.make()          # make the leaf, but make t_root first
    True
    >>> t_root.iscompleted()   # implicitly completed by make
    True
    >>> t_leaf.iscompleted()
    True

## Class `TaskError(cs.fsm.FSMError, builtins.Exception, builtins.BaseException)`

Raised by `Task` related errors.

## Class `TaskQueue`

A task queue for managing and running a set of related tasks.

Unlike `make` and `Task.make`, this is aimed at a "dispatch" worker
which dispatches individual tasks as required.

Example 1, put 2 dependent tasks in a queue and run:

     >>> t1 = Task("t1", lambda: print("t1"))
     >>> t2 = t1.then("t2", lambda: print("t2"))
     >>> q = TaskQueue(t1, t2)
     >>> for _ in q.run(): pass
     ...
     t1
     t2

Example 2, put 1 task in a queue and run.
The queue only runs the specified tasks:

     >>> t1 = Task("t1", lambda: print("t1"))
     >>> t2 = t1.then("t2", lambda: print("t2"))
     >>> q = TaskQueue(t1)
     >>> for _ in q.run(): pass
     ...
     t1

Example 2, put 1 task in a queue with `run_dependent_tasks=True` and run.
The queue pulls in the dependencies of completed tasks and also runs those:

     >>> t1 = Task("t1", lambda: print("t1"))
     >>> t2 = t1.then("t2", lambda: print("t2"))
     >>> q = TaskQueue(t1, run_dependent_tasks=True)
     >>> for _ in q.run(): pass
     ...
     t1
     t2

*Method `TaskQueue.__init__(self, *tasks, run_dependent_tasks=False)`*:
Initialise the queue with the supplied `tasks`.

*Method `TaskQueue.add(self, task)`*:
Add a task to the tasks managed by this queue.

*Method `TaskQueue.as_dot(self, name=None, **kw)`*:
Compute a DOT syntax graph description of the tasks in the queue.

*Method `TaskQueue.get(self)`*:
Pull a completed or an unblocked pending task from the queue.
Return the task or `None` if nothing is available.

The returned task is no longer tracked by this queue.

*Method `TaskQueue.run(self, runstate=None, once=False)`*:
Process tasks in the queue until the queue has no completed tasks,
yielding each task, immediately if `task.iscompleted()`
otherwise after `taks.dispatch()`.

An optional `RunState` may be provided to allow early termination
via `runstate.cancel()`.

An incomplete task is `dispatch`ed before `yield`;
ideally it will be complete when the yield happens,
but its semantics might mean it is in another state such as `CANCELLED`.
The consumer of `run` must handle these situations.

# Release Log



*Release 20230401*:
Add missing requirement to DISTINFO.

*Release 20230331*:
* Task: subclass BaseTask instead of (FSM, RunStateMixin).
* BaseTask.__init__: use @uses_runstate to ensure we've got a RunState.

*Release 20230217*:
Task: subclass HasThreadState, drop .current_task() class method.

*Release 20221207*:
* Pull out core stuff from Task into BaseTask, aids subclassing.
* BaseTask: explainatory docustring about unusual FSM_DEFAULT_STATE design choice.
* BaseTask.tasks_as_dot: express the edges using the node ids instead of their labels.
* BaseTask: new tasks_as_svg() method like tasks_as_dot() but returning SVG.

*Release 20220805*:
Initial PyPI release.
