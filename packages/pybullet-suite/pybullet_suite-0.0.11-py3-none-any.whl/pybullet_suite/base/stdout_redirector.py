from contextlib import contextmanager, redirect_stdout
import ctypes
import io
import os, sys
import tempfile

# https://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/
@contextmanager
def stdout_redirector(stream):
    # The original fd stdout points to. Usually 1 on POSIX systems.
    libc = ctypes.CDLL(None)
    original_stdout_fd = sys.stdout.fileno()
    c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')
    flag = None
    def _redirect_stdout(to_fd):
        """Redirect stdout to the given file descriptor."""
        # Flush the C-level buffer stdout
        libc.fflush(c_stdout)
        # Flush and close sys.stdout - also closes the file descriptor (fd)
        if getattr(sys.stdout, "_original_stdstream_copy", None) is not None:
            sys.stdout._original_stdstream_copy = None
        else:
            sys.stdout.close()
            
        # Make original_stdout_fd point to the same file as to_fd
        os.dup2(to_fd, original_stdout_fd)
        # Create a new sys.stdout that points to the redirected fd
        sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))

    # Save a copy of the original stdout fd in saved_stdout_fd
    saved_stdout_fd = os.dup(original_stdout_fd)
    try:
        # Create a temporary file and redirect stdout to it
        tfile = tempfile.TemporaryFile(mode='w+b')
        if getattr(sys.stdout, "_original_stdstream_copy", None) is not None:
            sys.stdout._original_stdstream_copy = None
            flag = "ipykernel"
            #os.dup2(std._original_stdstream_copy, __std__.fileno())
        
        
            libc.fflush(c_stdout)
            yield
            tfile.flush()
            tfile.seek(0, io.SEEK_SET)
            stream.write(tfile.read())

        #_redirect_stdout(tfile.fileno())
        # Yield to caller, then redirect stdout back to the saved fd
        #yield
        #_redirect_stdout(saved_stdout_fd)
        # Copy contents of temporary file to the given stream
        
    finally:
        if flag is not None:
            sys.stdout._original_stdstream_copy = original_stdout_fd
        tfile.close()
        os.close(saved_stdout_fd)



# @contextmanager
# def stdout_redirector(stream):
#     libc = ctypes.CDLL(None)
#     c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')
#     original_stdout_fd = sys.stdout.fileno()
#     tfile = tempfile.TemporaryFile(mode='w+b')
    
#     if getattr(sys.stdout, "_original_stdstream_copy", None) is not None:
#         print(sys.stdout._original_stdstream_copy)
#         os.dup2(sys.stdout._original_stdstream_copy, sys.__stdout__.fileno())
#         sys.stdout._original_stdstream_copy = None
    
#     #redirect
#     libc.fflush(c_stdout)
#     print(original_stdout_fd)
    #os.dup2(tfile, original_stdout_fd)

    # libc.fflush(c_stdout)
    # if getattr(sys.stdout, "_original_stdstream_copy", None) is not None:
    #     print("hello")
    
    # def _redirect_stdout(to_fd):
    #     """Redirect stdout to the given file descriptor."""
    #     # Flush the C-level buffer stdout
    #     libc.fflush(c_stdout)
    #     # Flush and close sys.stdout - also closes the file descriptor (fd)
    #     #sys.stdout.close()

    #     if getattr(sys.stdout, "_original_stdstream_copy", None) is not None:
    #         # redirect captured pipe back to original FD
    #         os.dup2(to_fd, original_stdout_fd)
    #         sys.stdout._original_stdstream_copy = None
    #     else:
    #         os.dup2(to_fd, original_stdout_fd)    
        
    #     #os.close(sys.stdout.fileno())
    #     # Make original_stdout_fd point to the same file as to_fd
    #     #os.dup2(to_fd, original_stdout_fd)
    #     # Create a new sys.stdout that points to the redirected fd
    #     sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))


    # # Save a copy of the original stdout fd in saved_stdout_fd
    # saved_stdout_fd = os.dup(original_stdout_fd)
    # try:
    #     # Create a temporary file and redirect stdout to it
    #     tfile = tempfile.TemporaryFile(mode='w+b')
    #     _redirect_stdout(tfile.fileno())
    #     # Yield to caller, then redirect stdout back to the saved fd
    #     yield
    #     _redirect_stdout(saved_stdout_fd)
    #     # Copy contents of temporary file to the given stream
    #     tfile.flush()
    #     tfile.seek(0, io.SEEK_SET)
    #     stream.write(tfile.read())
    # finally:
    #     tfile.close()
    #     os.close(saved_stdout_fd)
    #     sys.stdout = sys.__stdout__