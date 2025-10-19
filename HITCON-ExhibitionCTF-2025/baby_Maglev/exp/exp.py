from pwn import *

context.log_level = 'debug'

with open('./exp.js', "rb") as f:
    exp_js = f.read()
size = len(exp_js)

p = remote('localhost', 48763)

p.sendlineafter(b'Length:\n', str(size).encode())
p.send(exp_js)

p.interactive()
