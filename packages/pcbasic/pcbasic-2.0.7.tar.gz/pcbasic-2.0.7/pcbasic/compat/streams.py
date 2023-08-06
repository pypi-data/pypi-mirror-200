import sys
import io
import os
import codecs
import tempfile
import logging
from contextlib import contextmanager

from .base import PY2


class StreamWrapper(object):
    """Base class for delegated stream wrappers."""

    def __init__(self, stream):
        """Set up codec."""
        self._stream = stream

    def __getattr__(self, attr):
        return getattr(self._stream, attr)

    def __getstate__(self):
        return vars(self)

    def __setstate__(self, stdict):
        return vars(self).update(stdict)



def _open_named_devnull(name, mode):
    """Open a stream to /dev/null with the given stream name."""
    stream = StreamWrapper(open(os.devnull, mode))
    stream.name = name
    return stream


def fix_stdio():
    """Make sure sys.std* exist and are forgiving of errors."""
    # stdio may become None in GUI mode
    # fix them to devnull to ensure any i/o doesn't lead to crashes
    if not sys.stdin:
        sys.stdin = _open_named_devnull('<stdin>', 'r')
    if not sys.stdout:
        sys.stdout = _open_named_devnull('<stdout>', 'w')
    if not sys.stderr:
        sys.stderr = _open_named_devnull('<stderr>', 'w')

    if not PY2:
        # avoid UnicodeDecodeErrors when writing to terminal which doesn't support all of Unicode
        # e.g latin-1 locales or unsupported locales defaulting to ascii
        try:
            # this needs Python >= 3.7
            sys.stdout.reconfigure(errors='replace')
        except AttributeError:
            sys.stdout.__init__(sys.stdout.buffer, encoding=sys.stdout.encoding, errors='replace')
        try:
            sys.stderr.reconfigure(errors='replace')
        except AttributeError:
            sys.stderr.__init__(sys.stderr.buffer, encoding=sys.stderr.encoding, errors='replace')


if PY2:
    def is_writable_text_stream(stream):
        """Stream is a writable stream that expects unicode."""
        return isinstance(stream, (
            io.TextIOWrapper, io.StringIO,
            codecs.StreamReaderWriter, codecs.StreamWriter,
        ))

    def is_readable_text_stream(stream):
        """Stream is a readable stream that produces unicode."""
        return isinstance(stream, (
            io.TextIOWrapper, io.StringIO,
            codecs.StreamReaderWriter, codecs.StreamReader,
        ))
else:
    def is_writable_text_stream(stream):
        """Stream is a writable stream that expects unicode."""
        try:
            stream.write(u'')
        except TypeError:
            return False
        return True

    def is_readable_text_stream(stream):
        """Stream is a readable stream that produces unicode."""
        return isinstance(stream.read(0), type(u''))



# pause/quiet standard streams
# ----------------------------
# previously we had a version that redirected c-level streams, thereby catching non-python output
# based on https://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/
# or http://stackoverflow.com/questions/977840/redirecting-fortran-called-via-f2py-output-in-python/978264#978264
# however, that method either:
# - closes stdout/stderr, as in the above link; which means that any cached reference
#   to sys.stderr or sys.stdout now refers to a closed file, and leads to an IOError if flushed.
# - or doesn't close stdout/stderr, in which case the windows version of python 3 keeps a handle
#   to the old stdout, whcih is now an invalid handle, leading to a WindowsError when flushed.
#   background here:
#   - https://stackoverflow.com/questions/52373180/python-on-windows-handle-invalid-when-redirecting-stdout-writing-to-file
#   - https://stackoverflow.com/questions/902967/what-is-a-windows-handle/902969#902969
# it would be possible to set PYTHONLEGACYWINDOWSSTDIO and use the python2 code to deal with unicode output, but
# - at some point we'll want to get rid of all the python2 compatibility code
# - it would be duplicating the standard library's approach which has surely had more people looking at it
# i have tried to use close-stdout approach and fix all stale references, however new ones keep popping
# up e.g. in logging, unittest, curses. there are probably more, which means hard-to-debug future crashes
# the only reason to redirect c-level stream were:
# - pyaudio on alsa produces a lot of chatter on init which is annoying on a console interface
# - pygame prints a "banner" message to the console when imported, which is annoying especially when using another interface
# since:
# - the first is annoying but does not deface the screen during runtime
# - the second only occurs in a deprecated interface, and can be avoided in other interfaces by delaying module load until it's needed
# - the whole thing is a bit hacky and clearly likely to break in newer python versions
# - there are probably still crashes hidden away in some code paths
# all of this is an unreasonable maintenance load and it is better to go with the supported method
# of doing a "shallow" redirect by reassigning sys.std***.


class StdIOBase(object):
    """Holds standard unicode streams."""

    def __init__(self):
        self._attach_stdin()
        self._attach_output_stream('stdout')
        self._attach_output_stream('stderr')

    def _attach_stdin(self):
        # stdio becomes None in GUI mode
        # use __stdin__ as we depend elsewhere on this having a .buffer and pointing to true stdin
        self.stdin = sys.__stdin__ or _open_named_devnull('<stdin>', 'r')

    def _attach_output_stream(self, stream_name, redirected=False):
        # stdio becomes None in GUI mode
        stream = getattr(sys, '__%s__' % (stream_name,))
        if not stream:
            stream = _open_named_devnull('<%s>' % (stream_name,), 'w')
        setattr(self, stream_name, stream)

    # unicode stream wrappers

    def _wrap_output_stream(self, stream, encoding=None):
        """Wrap std bytes streams or redirected files to make them behave more like in Python 3."""
        encoding = encoding or stream.encoding or 'utf-8'
        wrapped = codecs.getwriter(encoding)(stream, errors='replace')
        wrapped.buffer = stream
        return wrapped

    def _wrap_input_stream(self, stream, encoding=None):
        """Wrap std bytes streams or redirected files to make them behave more like in Python 3."""
        encoding = encoding or stream.encoding or 'utf-8'
        wrapped = codecs.getreader(encoding)(stream)
        wrapped.buffer = stream
        return wrapped

    @contextmanager
    def _muffle_one(self, stream_name, preserve, redirect):
        """Silence stdout or stderr. On Python 2, also silences external writes."""
        std_stream = getattr(sys, '__%s__' % (stream_name,))
        if not PY2:
            encoding = std_stream.encoding
        save = None
        try:
            if not PY2:
                save_buffer = std_stream.buffer
            else: # pragma: no cover
                try:
                    # save the file descriptor for the target stream
                    save = os.dup(std_stream.fileno())
                except EnvironmentError as e:
                    # won't work, give up
                    logging.error(e)
                    yield
                    return
            if preserve or redirect:
                temp_file = tempfile.TemporaryFile('w+b')
            else:
                temp_file = io.open(os.devnull, 'wb')
            with temp_file as temp:
                std_stream.flush()
                if not PY2:
                    # replace the underlying buffer in the TextIOWrapper
                    # since we're mutating the object, affects all stored references.
                    std_stream.__init__(temp_file, encoding=encoding) # errors='replace'
                else: # pragma: no cover
                    # the old unix way, doesn't work on python3.6+/windows
                    # put /dev/null fds on 1 (stdout) or 2 (stderr)
                    os.dup2(temp.fileno(), std_stream.fileno())
                # fix our own streams - needed on Windows
                # as we keep a hacked stream writing to the Windows API
                self._attach_output_stream(stream_name, redirected=True)
                # do stuff
                try:
                    yield
                finally:
                    std_stream.flush()
                    # restore file descriptors
                    if not PY2:
                        std_stream.__init__(save_buffer, encoding=encoding)
                    else: # pragma: no cover
                        os.dup2(save, std_stream.fileno())
                    self._attach_output_stream(stream_name, redirected=False)
                    if preserve:
                        if PY2: # pragma: no cover
                            redirect = std_stream
                        else:
                            redirect = std_stream.buffer
                    if redirect:
                        # write contents of temporary file into redirect or back into standard io
                        temp.flush()
                        temp.seek(0)
                        redirect.write(temp.read())
        finally:
            if save is not None:
                os.close(save)

    @contextmanager
    def _muffle(self, stream_name, **kwargs):
        """Silence stdout, stderr, or both."""
        if not stream_name:
            with self._muffle_one('stdout', **kwargs):
                with self._muffle_one('stderr', **kwargs):
                    yield
        else:
            with self._muffle_one(stream_name, **kwargs):
                yield

    @contextmanager
    def pause(self, stream_name=None):
        """Pause stdout or stderr or both, preserving output."""
        with self._muffle(stream_name, preserve=True, redirect=None):
            yield

    @contextmanager
    def quiet(self, stream_name=None):
        """Pause stdout or stderr or both, not preserving output."""
        with self._muffle(stream_name, preserve=False, redirect=None):
            yield

    @contextmanager
    def redirect_output(self, output=None, stream_name=None):
        """Pause stdout or stderr or both, redirecting output."""
        with self._muffle(stream_name, preserve=False, redirect=output):
            yield
