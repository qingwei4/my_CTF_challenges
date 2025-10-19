# my_CTF_challenges

### HITCON-ExhibitionCTF-2025 / baby Maglev
Exploit a HeapNumber UAF in V8

### bof1
```
Ubuntu 20.04
```
stack buffer overflow, ret2win

### bof2
```
Ubuntu 20.04
```
exploit read() to leak infomation, partial overwrite, ret2libc

### fmt
```
Ubuntu 20.04
```
exploit printf() to leak infomation, ret2libc

### fastbin_dup
```
Ubuntu 20.04
```
fastbin_dup, stash into tcache, hijack __malloc_hook

### off-by-null
```
Ubuntu 18.04
```
off-by-null overflow, hijack __free_hook

### CGGC 2023/gift
```
Ubuntu 20.04
```
hijack __stack_chk_fail() then ret2libc

### CGGC 2023/note
```
Ubuntu 20.04
```
exploit off-by-one on heap

### CGGC 2024/CGGC_allocator
use large bin attack to hijack _IO_list_all, then FSOP

### CGGC 2024/baby overflow
Heap feng shui to leak address, then use heap overflow to RCE

### TSCCTF 2025 / noview
Overwrite \_IO_2_1_stdout_ to leak libc address then use UAF to RCE
### TSCCTF 2024 / babyheap
leak libc address via unsorted bin directly, then use heap overflow to get RCE
