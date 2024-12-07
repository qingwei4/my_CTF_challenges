Gift (easy)
---
You have a bof and arbitrary write. PIE is off and Canary is on.
use arbitrary write to overwrite __stack_chk_fail to 0x40101a (ret).
Now you defeat stack canary, ROP to leak libc address and get shell.

note (medium)
---
### Step 1. leak libc
scanf("%d", &n) use heap as buffer when n is very large, before scanf() return, it will merge chunks in fastbin into smallbin.
you can allocate that chunk and show that note to leak libc address

### Step 2. construct overlapped chunks
there is a off-by-one overflow in input(), you can use it to overwrite size in chunk header.
free it and allocate it back, the chunk is extended so you have a heap overflow.

### Step 3. get shell
You can overwrite *next in tcache now!
Use tcache poisoning to allocate a chunk at __free_hook, overwrite it to system.
Delete a chunk which has '/bin/sh\x00' on it will trigger system("/bin/sh\x00") and give you a shell.
