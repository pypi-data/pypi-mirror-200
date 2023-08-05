"""
This module creates a temporary file that will hold all partitions.
"""


from Viper.abc.io import BytesIO
from Viper.meta.secret import secret
from threading import Lock
from io import SEEK_SET

__all__ = ["Partition", "alloc"]





PACKETSIZE = 2 ** 20
BASESIZE = 2 ** 10

class VirtualFile(BytesIO):

    """
    This class implements virtual temporary files. They do not match any specific file in the file system and behaves like temporary files.
    """

    def __init__(self, part : "Partition", descriptor : int) -> None:
        self.__part = part
        self.__desc = descriptor
        self.__file = part.file
        self.__pointer = part.address(descriptor).start
        self.__lock = part.lock
        self.__end = self.__pointer
        
    def fileno(self) -> int:
        """
        A VirtualFile has no file descriptor.
        """
        raise FileNotFoundError("VirtualFile has no file descriptor")
    
    def close(self):
        with self.__lock:
            self.__lock = None
            self.__part.free(self.__desc)
    
    @property
    def closed(self) -> bool:
        return self.__lock == None
    
    def tell(self) -> int:
        with self.__lock:
            r = self.__part.address(self.__desc)
            return self.__pointer - r.start
    
    def seekable(self) -> bool:
        return True
    
    def seek(self, offset: int, whence: int = SEEK_SET, /) -> int:
        from io import SEEK_CUR, SEEK_END, SEEK_SET
        if not isinstance(offset, int) or not isinstance(whence, int):
            raise TypeError("Expected int, int, got " + repr(type(offset).__name__) + " and " + repr(type(whence).__name__))
        if whence not in (SEEK_CUR, SEEK_END, SEEK_SET):
            raise ValueError("whence must be in " + str((SEEK_CUR, SEEK_END, SEEK_SET)))
        with self.__lock:
            r = self.__part.address(self.__desc)
            if whence == SEEK_SET:
                if offset < 0:
                    raise OSError("Invalid argument")
                self.__pointer = r.start + offset
            elif whence == SEEK_END:
                if r.stop + offset < r.start:
                    raise OSError("Invalid argument")
                self.__pointer = r.stop + offset
            elif whence == SEEK_CUR:
                if self.__pointer + offset < r.start:
                    raise OSError("Invalid argument")
                self.__pointer += offset
            return 
    
    def read_blocking(self) -> bool:
        return False

    def read(self, size: int = -1, /) -> bytes:
        if not isinstance(size, int):
            raise TypeError("Expected int, got " + repr(type(size).__name__))
        if size < -1:
            raise ValueError("read length must be non-negative or -1")
        if self.closed:
            raise ValueError("read of closed file")
        with self.__lock:
            self.__file.seek(self.__pointer)
            if size < 0:
                size = float("inf")
            amount = min(self.__end - self.__pointer, size)
            data = self.__file.read(amount)
            self.__pointer += len(data)
            return data
    
    def readinto(self, buffer: bytearray | memoryview, /) -> int:
        if not isinstance(buffer, (bytearray, memoryview)):
            raise TypeError("Expected writable buffer, got " + repr(type(buffer).__name__))
        if self.closed:
            raise ValueError("readinto of closed file")
        with self.__lock:
            size = len(buffer)
            self.__file.seek(self.__pointer)
            if size < 0:
                size = float("inf")
            amount = min(self.__end - self.__pointer, size)
            data = self.__file.readinto(amount)
            buffer[:len(data)] = data
            self.__pointer += len(data)
            return len(data)
    
    def readline(self, size: int = -1, /) -> bytes:
        if not isinstance(size, int):
            raise TypeError("Expected int, got " + repr(type(size).__name__))
        if size < -1:
            raise ValueError("read length must be non-negative or -1")
        if self.closed:
            raise ValueError("readline of closed file")
        with self.__lock:
            self.__file.seek(self.__pointer)
            if size < 0:
                size = float("inf")
            amount = min(self.__end - self.__pointer, size)
            data = self.__file.readline(amount)
            self.__pointer += len(data)
            return data
    
    async def aread(self, size: int = -1, /) -> bytes:
        return self.read(size)
    
    async def areadinto(self, buffer: bytearray | memoryview, /) -> int:
        return self.readinto(buffer)
    
    def write_blocking(self) -> bool:
        return False
    
    def flush(self):
        if self.closed:
            raise ValueError("flush of closed file")
        return self.__file.flush()
    
    def truncate(self, size: int | None = None, /):
        if size != None and not isinstance(size, int):
            raise TypeError("Expected int or None, got " + repr(type(size).__name__))
        if self.closed:
            raise ValueError("truncate of closed file")
        from io import SEEK_END
        with self.__lock:
            r = self.__part.address(self.__desc)
            old_size = self.__end - r.start
            if size <= old_size:
                self.__end = r.start + size
            else:
                if size > len(r):
                    self.__part.resize(self.__desc, size * 2)
                    old_start = r.start
                    r = self.__part.address(self.__desc)
                    self.__pointer = r.start + (self.__pointer - old_start)
                    self.__end = r.start + (self.__end - old_start)
                self.__file.seek(self.__end)
                i = old_size
                while i < size:
                    data = b"\0" * min(PACKETSIZE, size - i)
                    self.__file.write(data)
                    i += PACKETSIZE
                self.__file.seek(0, SEEK_END)
                total_size = self.__file.tell()
                self.__end = r.start + size
                if total_size < self.__end:
                    self.__file.truncate(self.__end)
    
    def write(self, data: bytes | bytearray | memoryview, /) -> int:
        if not isinstance(data, bytes | bytearray | memoryview):
            raise TypeError("Expected readable buffer, got " + repr(type(data).__name__))
        if self.closed:
            raise ValueError("write of closed file")
        with self.__lock:
            r = self.__part.address(self.__desc)
            if self.__pointer + len(data) not in r:
                self.__part.resize(self.__desc, (len(r) + len(data)) * 2)
                old_start = r.start
                r = self.__part.address(self.__desc)
                self.__pointer = r.start + (self.__pointer - old_start)
                self.__end = r.start + (self.__end - old_start)
            self.__file.seek(self.__pointer)
            n = self.__file.write(data)
            self.__pointer += n
            self.__end = max(self.__end, self.__pointer)
            return n
    
    async def awrite(self, data: bytes | bytearray | memoryview, /) -> int:
        return self.write(data)
    

    

    


class Partition:

    """
    A partitionned file. References a temporary file and holds a partionning of the file space.
    """

    def __init__(self) -> None:
        from threading import RLock
        from tempfile import mkstemp
        from os import fdopen
        self.__desc, self.__path = mkstemp()
        print("New temp file :", self.__path)
        self.__file = fdopen(self.__desc, "w+b", buffering=0)
        self.__pagetable : dict[int, range] = {}
        self.__inverted_pagetable : dict[range, int] = {}
        self.__sorted_ranges : list[range] = []
        self.__lock = RLock()
    
    @property
    def ranges(self) -> list[range]:
        return self.__sorted_ranges.copy()
    
    def show(self):
        with self.lock:
            self.__file.seek(0)
            print(self.__file.read())
        
    def alloc(self, size : int = BASESIZE) -> VirtualFile:
        """
        Allocates space in the partition for a virtual file.
        """
        if not isinstance(size, int):
            raise TypeError("Expected int, got " + repr(type(size).__name__))
        if size <= 0:
            raise TypeError("Expected positive size, got " + repr(size))
        with self.__lock:
            last = 0
            new_range = None
            for i, r in enumerate(self.__sorted_ranges):
                if r.start - last >= size:
                    new_range = range(last, last + size)
                    break
                last = r.stop
            if not new_range:
                new_range = range(last, last + size)
                i = len(self.__sorted_ranges)
            desc = len(self.__pagetable)
            while desc in self.__pagetable:
                desc += 1
            self.__pagetable[desc] = new_range
            self.__inverted_pagetable[new_range] = desc
            self.__sorted_ranges.insert(i, new_range)
            return VirtualFile(self, desc)

    def resize(self, descriptor : int, size : int = BASESIZE):
        """
        Resizes the space allocated for the given file descriptor. The given size is the absolute size.
        It also copies data from old buffer to new and erases old buffer.
        """
        from os import urandom
        if not isinstance(size, int) or not isinstance(descriptor, int):
            raise TypeError("Expected int, int, got " + repr(type(descriptor).__name__) + " and " + repr(type(size).__name__))
        if size <= 0:
            raise TypeError("Expected positive size, got " + repr(size))
        with self.__lock:
            if descriptor not in self.__pagetable:
                raise FileNotFoundError("Could not find given file.")
            r1 = self.__pagetable[descriptor]
            i = self.__sorted_ranges.index(r1)
            if i + 1 == len(self.__sorted_ranges):
                new_range = range(r1.start, r1.start + size)
                j = i
            else:
                r2 = self.__sorted_ranges[i + 1]
                if size < r2.start - r1.start:
                    new_range = range(r1.start, r1.start + size)
                    j = i
                else:
                    new_range = range(self.__sorted_ranges[-1].stop, self.__sorted_ranges[-1].stop + size)
                    j = len(self.__sorted_ranges)
            self.__sorted_ranges.pop(i)
            self.__sorted_ranges.insert(j, new_range)
            self.__pagetable[descriptor] = new_range
            self.__inverted_pagetable.pop(r1)
            self.__inverted_pagetable[new_range] = descriptor
            k = 0
            new_size = min(len(r1), len(new_range))
            while k < new_size:
                self.__file.seek(r1.start + k)
                data = self.__file.read(min(PACKETSIZE, new_size - k))
                self.__file.seek(new_range.start + k)
                self.__file.write(data)
                k += PACKETSIZE
            self.__file.seek(r1.start)
            i = 0
            while i < len(r1):
                self.__file.write(urandom(min(PACKETSIZE, len(r1) - i)))
                i += PACKETSIZE
    
    def free(self, descriptor : int):
        """
        Frees space allocated for the given file descriptor.
        It also erases data that was previously written.
        """
        from os import urandom
        if not isinstance(descriptor, int):
            raise TypeError("Expected int, got " + repr(type(descriptor).__name__))
        with self.__lock:
            if descriptor not in self.__pagetable:
                raise FileNotFoundError("Could not find given file.")
            r = self.__pagetable.pop(descriptor)
            self.__inverted_pagetable.pop(r)
            self.__sorted_ranges.remove(r)
            self.__file.seek(r.start)
            i = 0
            while i < len(r):
                self.__file.write(urandom(min(PACKETSIZE, len(r) - i)))
                i += PACKETSIZE
    
    def address(self, descriptor : int) -> range:
        """
        Returns the address range for the associated file descriptor.
        """
        if not isinstance(descriptor, int):
            raise TypeError("Expected int, got " + repr(type(descriptor).__name__))
        with self.__lock:
            if descriptor not in self.__pagetable:
                raise FileNotFoundError("Could not find given file.")
            return self.__pagetable[descriptor]
    
    @property
    def lock(self) -> Lock:
        """
        Returns the lock on the partition.
        """
        return self.__lock
    
    @property
    def file(self) -> BytesIO:
        """
        Returns a file wrapper to the actual partitionned file.
        """
        from os import fdopen
        return fdopen(self.__desc, "w+b", buffering=0)
    
    def __del__(self):
        """
        Implements destruction of self.
        """
        from os import remove, close
        close(self.__desc)
        remove(self.__path)



PART = Partition()



@secret(PART)
def alloc(part : Partition, size : int = BASESIZE) -> VirtualFile:
    """
    Creates a VirtualFile in a module-level partition, with given size allocated at creation.
    """
    if not isinstance(size, int):
        raise TypeError("Expected int, got " + repr(type(size).__name__))
    if size < 0:
        raise ValueError("Cannot alloc VirtualFile of negative size")
    return part.alloc(size)





del PART, BytesIO, secret, Lock, SEEK_SET