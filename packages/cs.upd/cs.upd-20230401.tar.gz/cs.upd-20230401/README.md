Single and multiple line status updates with minimal update sequences.

*Latest release 20230401*:
* Upd.run_task: use a local RunState to control the ticker, drop `runstate` parameter.
* Renamed default HasThreadState.THREAD_STATE_ATTR to 'perthread_state'.
* Keep a module level name for the default Upd instance.
* Upd.shutdown: cope with shutdown early enough that there's no self._lock.
* Honour new $CS_UPD_BACKEND envvar to support eg defaulting Upd to /dev/null.

This is available as an output mode in `cs.logutils`.

Single line example:

    from cs.upd import Upd, nl, print
    .....
    with Upd() as U:
        for filename in filenames:
            U.out(filename)
            ... process filename ...
            U.nl('an informational line to stderr')
            print('a line to stdout')

Multiline multithread example:

    from threading import Thread
    from cs.upd import Upd, print
    .....
    def runner(filename, proxy):
        # initial status message
        proxy.text = "process %r" % filename
        ... at various points:
            # update the status message with current progress
            proxy.text = '%r: progress status here' % filename
        # completed, remove the status message
        proxy.close()
        # print completion message to stdout
        print("completed", filename)
    .....
    with Upd() as U:
        U.out("process files: %r", filenames)
        Ts = []
        for filename in filenames:
            proxy = U.insert(1) # allocate an additional status line
            T = Thread(
                "process "+filename,
                target=runner,
                args=(filename, proxy))
            Ts.append(T)
            T.start()
        for T in Ts:
            T.join()

## A note about Upd and terminals

I routinely use an `Upd()` as a progress reporting tool for commands
running on a terminal. This attaches to `sys.stderr` by default.
However, it is usually not desirable to run an `Upd` display
if the backend is not a tty/terminal.
Therefore, an `Upd` has a "disabled" mode
which performs no output;
the default behaviour is that this mode activates
if the backend is not a tty (as tested by `backend.isatty()`).
The constructor has an optional parameter `disabled` to override
this default behaviour.

## Function `demo()`

A tiny demo function for visual checking of the basic functionality.

## Class `Upd(cs.obj.SingletonMixin, cs.resources.MultiOpenMixin, cs.threads.HasThreadState, cs.context.ContextManagerMixin)`

A `SingletonMixin` subclass for maintaining multiple status lines.

The default backend is `sys.stderr`.

*Method `Upd.__init__(self, backend=None, columns=None, disabled=None)`*:
Initialise the `Upd`.

Parameters:
* `backend`: the output file, default from the environment
  variable `$CS_UPD_BACKEND` otherwise `sys.stderr`
* `columns`: the width of the output,
  default from the width of the `backend` tty if it is a tty,
  `80` otherwise
* `disabled`: if true, disable the output - just keep state;
  default true if the output is not a tty;
  this automatically silences the `Upd` if stderr is not a tty

*Method `Upd.__enter_exit__(self)`*:
Generator supporting `__enter__` and `__exit__`.

On shutdown, if we are exiting because of an exception
which is not a `SystemExit` with a `code` of `None` or `0`
then we preserve the status lines one screen.
Otherwise we clean up the status lines.

*Method `Upd.__getitem__(self, index)`*:
The text of the status line at `index`.

*Method `Upd.__len__(self)`*:
The length of an `Upd` is the number of slots.

*Method `Upd.above(self, need_newline=False)`*:
Context manager to move to the top line of the display, clear it, yield, redraw below.

This context manager is for use when interleaving _another_
stream with the `Upd` display;
if you just want to write lines above the display
for the same backend use `Upd.nl`.

The usual situation for `Upd.above`
is interleaving `sys.stdout` and `sys.stderr`,
which are often attached to the same terminal.

Note that the caller's output should be flushed
before exiting the suite
so that the output is completed before the `Upd` resumes.

Example:

    U = Upd()   # default sys.stderr Upd
    ......
    with U.above():
        print('some message for stdout ...', flush=True)

*Method `Upd.cursor_invisible(self)`*:
Make the cursor vinisible.

*Method `Upd.cursor_visible(self)`*:
Make the cursor visible.

*Method `Upd.delete(self, index)`*:
Delete the status line at `index`.

Return the `UpdProxy` of the deleted status line.

*Method `Upd.diff(oldtxt, newtxt, columns, raw_text=False)`*:
Compute the text sequences required to update `oldtxt` to `newtxt`
presuming the cursor is at the right hand end of `oldtxt`.
The available area is specified by `columns`.

We normalise `newtxt` as using `self.normalise`.
`oldtxt` is presumed to be already normalised.

If `raw_text` is true (default `False`) we do not normalise `newtxt`
before comparison.

*Method `Upd.disable(self)`*:
Disable updates.

*Property `Upd.disabled`*:
Whether this `Upd` is currently disabled.

*Method `Upd.enable(self)`*:
Enable updates.

*Method `Upd.flush(self)`*:
Flush the backend stream.

*Method `Upd.insert(self, index, txt='', proxy=None, **proxy_kw) -> 'UpdProxy'`*:
Insert a new status line at `index`.
Return the `UpdProxy` for the new status line.

*Method `Upd.nl(self, txt, *a, redraw=False)`*:
Write `txt` to the backend followed by a newline.

Parameters:
* `txt`: the message to write.
* `a`: optional positional parameters;
  if not empty, `txt` is percent formatted against this list.
* `redraw`: if true (default `False`) use the "redraw" method.

This uses one of two methods:
* insert above:
  insert a line above the top status line and write the message there.
* redraw:
  clear the top slot, write txt and a newline,
  redraw all the slots below.

The latter method is used if `redraw` is true
or if `txt` is wider than `self.columns`
or if there is no "insert line" capability.

*Method `Upd.normalise(txt)`*:
Normalise `txt` for display,
currently implemented as:
`unctrl(txt.rstrip())`.

*Method `Upd.out(self, txt, *a, slot=0, raw_text=False, redraw=False) -> str`*:
Update the status line at `slot` to `txt`.
Return the previous status line content.

Parameters:
* `txt`: the status line text.
* `a`: optional positional parameters;
  if not empty, `txt` is percent formatted against this list.
* `slot`: which slot to update; default is `0`, the bottom slot
* `raw_text`: if true (default `False`), do not normalise the text
* `redraw`: if true (default `False`), redraw the whole line
  instead of doing the minimal and less visually annoying
  incremental change

*`Upd.perthread_state`*

*Method `Upd.proxy(self, index)`*:
Return the `UpdProxy` for `index`.
Returns `None` if `index` is out of range.
The index `0` is never out of range;
it will be autocreated if there are no slots yet.

*Method `Upd.run_task(self, label: str, report_print=False, tick_delay: int = 0.3, tick_chars='|/-\\')`*:
Context manager to display an `UpdProxy` for the duration of some task.
It yields the proxy.

*Method `Upd.selfcheck(self)`*:
Sanity check the internal data structures.

Warning: this uses asserts.

*Method `Upd.shutdown(self, preserve_display=False)`*:
Clean out this `Upd`, optionally preserving the displayed status lines.

*Method `Upd.ti_str(self, ti_name)`*:
Fetch the terminfo capability string named `ti_name`.
Return the string or `None` if not available.

*Method `Upd.without(self, temp_state='', slot=0)`*:
Context manager to clear the status line around a suite.
Returns the status line text as it was outside the suite.

The `temp_state` parameter may be used to set the inner status line
content if a value other than `''` is desired.

## Class `UpdProxy`

A proxy for a status line of a multiline `Upd`.

This provides a stable reference to a status line after it has been
instantiated by `Upd.insert`.

The status line can be accessed and set via the `.text` property.

An `UpdProxy` is also a context manager which self deletes on exit:

    U = Upd()
    ....
    with U.insert(1, 'hello!') as proxy:
        .... set proxy.text as needed ...
    # proxy now removed

*Method `UpdProxy.__call__(self, msg, *a)`*:
Calling the proxy sets its `.text` property
in the form used by other messages: `(msg,*a)`

*Method `UpdProxy.__del__(self)`*:
Delete this proxy from its parent `Upd`.

*Method `UpdProxy.delete(self)`*:
Delete this proxy from its parent `Upd`.

*Method `UpdProxy.extend_prefix(self, more_prefix, print_elapsed=False)`*:
Context manager to append text to the prefix.

*Method `UpdProxy.insert(self, index, txt='')`*:
Insert a new `UpdProxy` at a position relative to this `UpdProxy`.
Return the new proxy.

This supports the positioning of related status lines.

*Property `UpdProxy.prefix`*:
The current prefix string.

*Method `UpdProxy.reset(self)`*:
Clear the proxy: set both the prefix and text to `''`.

*Property `UpdProxy.suffix`*:
The current suffix string.

*Property `UpdProxy.text`*:
The text of this proxy's slot, without the prefix.

*Property `UpdProxy.width`*:
The available space for text after `self.prefix` and before `self.suffix`.

This is available width for uncropped text,
intended to support presizing messages such as progress bars.
Setting the text to something longer will crop the rightmost
portion of the text which fits.

## Function `uses_upd(func)`

Decorator for functions accepting an optional `upd:Upd` parameter,
default from `Upd.default() or Upd()`.
This also makes the `upd` the default `Upd` instance for this thread.

## Function `with_upd_proxy(*da, **dkw)`

Decorator to run `func` with an additional parameter `upd_proxy`
being an `UpdProxy` for progress reporting.

Example:

    @with_upd_proxy
    def func(*a, upd_proxy:UpdProxy, **kw):
      ... perform task, updating upd_proxy ...

# Release Log



*Release 20230401*:
* Upd.run_task: use a local RunState to control the ticker, drop `runstate` parameter.
* Renamed default HasThreadState.THREAD_STATE_ATTR to 'perthread_state'.
* Keep a module level name for the default Upd instance.
* Upd.shutdown: cope with shutdown early enough that there's no self._lock.
* Honour new $CS_UPD_BACKEND envvar to support eg defaulting Upd to /dev/null.

*Release 20230217*:
* @uses_upd: provide Upd() if there is no current default.
* @uses_upd: set the default Upd to the chosen Upd instance.
* Upd: subclass MultiOpenMixin, drop close() and closed() methods; always make a default Upd instance in open state.
* Upd: always define an initial slot and its UpdProxy, avoids a billion special cases elsewhere.
* UpdProxy: accept index=None as "make a bare UpdProxy for upd" used in the Upd._reset setup code, reserving the magic self inserting mode for when index is not None.

*Release 20230212*:
* BREAKING: replace @upd_proxy (which fiddled upd.state) with @with_upd_proxy which supplies an upd_proxy parameter.
* UpdProxy.text: bugfix spelling of _text_auto.
* Upd now subclasses HasThreadState, replace global "state" with "Upd.state", related adjustments.
* UpdProxy: new optional update_period parameter to limit the update frequency based on the time since last update.
* Upd.insert: support keyword parameters for the created UpdProxy.

*Release 20221228*:
Bugfix print: plumb the end= parameter.

*Release 20220918*:
* DROPPING PYTHON 2 SUPPORT.
* New @uses_upd decorator for things accepting an optional upd=Upd().
* UpdProxy.__init__: use @uses_upd, make text the only optional positional parameter.
* New top level `run_task` context manager wrapping `Upd.run_task`.
* Make all the top level functions accept an optional upd=Upd() parameter.
* Upd.run_task: wrap the yield in a try/finally to manage the RunState.
* Upd.run_task: set default tick_delay=0.3, 0.15 was too fast.
* UpdProxy: new optional text_auto() callable parameter, used to compute proxy.text if proxy._text is empty.
* UpdProxy.width: account for the suffix.

*Release 20220619*:
Upd.cursor_visible,cursor_invisible: actually send the escape sequence.

*Release 20220606*:
Upd.insert: insert(1) on empty slots autocreates slot 0.

*Release 20220605*:
* New Upd.run_task to add a status line for the duration of some task.
* UpdProxy.extend_prefix: new optional print_elapsed parameter.

*Release 20220530*:
* UpdProxy: new .suffix property.
* Upd: new run_task context manager to display an UpdProxy while something runs, with optional ticker.
* Small bugfix.

*Release 20220504*:
* Upd.above: do a disable/enable around the yield, use try/finally for reliability.
* Upd.delete: just warn about index out of range, seems it can happen during interpreter shutdown; to be debugged later.

*Release 20220429*:
* UpdProxy: accept optional prefix= parameter.
* New pfxprint wrapper for cs.pfx.pfxprint, like the print wrapper.

*Release 20210717*:
Docstring update.

*Release 20210507*:
Upgrade dependency on cs.context for StackableState.

*Release 20210428.4*:
Another dummy release during debugging.

*Release 20210428.3*:
Repeat the previous release, again again.

*Release 20210428.2*:
Repeat the previous release, again.

*Release 20210428.1*:
Repeat the previous release.

*Release 20210428*:
Do curses.setupterm() during iinit, avoid failure when stdout is not a tty.

*Release 20210316*:
* New UpdProxy.extend_prefix context manager to extend the proxy prefix around a suite.
* New global "state" StackableStatei object with an automatic .upd attribute.
* New @upd_proxy decorator to create an UpdProxy for the duration of a function call and record it as state.proxy.
* Bugfix Upd.insert: add slots.insert and proxies.insert missing from the no-display path.
* Rename private method Upd._adjust_text_v to public method Upd.diff.

*Release 20210122*:
* Autocreate slot 0 on first use.
* Reliable cleanup at exit.
* Fix a display small display issue.

*Release 20201202*:
* Fix for batch mode - handle failure of curses.setupterm(), throws TypeError.
* Upd.insert: defer check for cuu1 capability until there's at least one line already.

*Release 20201102*:
* Upd.nl: simple approach when there are no status lines.
* Upd: new cursor_visible and cursor_invisible methods to show and hide the cursor.

*Release 20201026.1*:
Bugfix Upd.nl: simple output if there are no status lines to accomodate.

*Release 20201026*:
Bugfix Upd.insert: accept insert(1) when len(self)==0.

*Release 20201025*:
* Upd: new .disabled property to allow inspection of disabledness.
* Upd.insert: accept negative insert indices to position from the top of the list.
* Upd.nl: use clear-to-end-of-line at the end of the message if available.
* UpdProxy: turn .prefix into a property which causes a redraw when changed.
* Upd.proxy(index): return None if the index is out of range, accomodates racy or incorrect behaviour by a user.
* UpdProxy: cropped overflowing text gets a leading '<' to make it apparent.
* UpdProxy: new .insert() method to support insterting new proxies with respect to an existing proxy.
* UpdProxy: new reset() method, clears prefix and text.
* UpdProxy.__init__: BREAKING: make all arguments optional to aid use.
* Upd: do not make any slots unless required.
* Make the compute-redraw-strings methods private.

*Release 20200914*:
Bugfix UpdProxy.__enter__: return self.

*Release 20200716.1*:
DISTINFO: make the cs.obj requirement more specific due to the SingletonMixin API change.

*Release 20200716*:
Update for changed cs.obj.SingletonMixin API.

*Release 20200626.1*:
Upd.__exit__: bugfix test of SystemExit exceptions.

*Release 20200626*:
* UpdProxy: call self.delete on __del__.
* If self._backend is None act as if disabled, occurs during shutdown.
* Upd.delete: ignore attempts to delete the last line, also occurs during shutdown.

*Release 20200621*:
New "disabled" mode, triggered by default if not backend.isatty().

*Release 20200613*:
* New UpdProxy.__call__ which sets the .text property in the manner of logging calls, with (msg,*a).
* New Upd.normalise static method exposing the text normalisation `unctrl(text.rstrip())`.
* New UpdProxy.prefix attribute with a fixed prefix for status updates; `prefix+text` is left cropped for display purposes when updated.
* New UpdProxy.width property computing the space available after the prefix, useful for sizing things like progress bars.
* Make UpdProxy a context manager which self deletes on exit.
* Upd: make default backend=sys.stderr, eases the common case.
* New Upd.above() context manager to support interleaving another stream with the output, as when stdout (for print) is using the same terminal as stderr (for Upd).
* New out() top level function for convenience use with the default Upd().
* New nl() top level function for writing a line to stderr.
* New print() top level function wrapping the builtin print; callers can use "from cs.upd import print" to easily interleave print() with cs.upd use.

*Release 20200517*:
* Multiline support!
* Multiline support!
* Multiline support!
* New UpdProxy class to track a status line of a multiline Upd in the face of further inserts and deletes.
* Upd(...) now returns a context manager to clean up the display on its exit.
* Upd(...) is now a SingletonMixin in order to use the same state if set up in multiple places.

*Release 20200229*:
* Upd: can now be used as a context manager, clearing the line on exit.
* Upd.without is now a context manager, returning the older state, and accepting an optional inner state (default "").
* Upd is now a singleton factory, obsoleting upd_for.
* Upd.nl: use "insert line above" mode if supported.

*Release 20181108*:
Documentation improvements.

*Release 20170903*:
* New function upd_for(stream) returning singleton Upds.
* Drop noStrip keyword argument/mode - always strip trailing whitespace.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* Add Upd.flush method.
* Upd.out: fix longstanding trailing text erasure bug.
* Upd.nl,out: accept optional positional parameters, use with %-formatting if supplied, just like logging.

*Release 20150118*:
metadata fix

*Release 20150116*:
Initial PyPI release.
