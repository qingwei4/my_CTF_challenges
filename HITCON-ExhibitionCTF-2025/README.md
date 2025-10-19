Baby Maglev
---

Inspired by CVE-2025-9864

### TL;DR : Exploit a UAFed Heap Number in V8

baby_Maglev/chal : The challenge attachments, including a patch and a compiled V8 shell(d8)

baby_Maglev/exp/exp.js : Full exploit


### Patch Analysis
In MaglevReducer::GetTaggedValue(), this patch changes Float64ToTagged::ConversionMode from kCanonicalizeSmi to kForceHeapNumber.

Float64ToTagged::ConversionMode::kCanonicalizeSmi will use smi to store the value when the value fits into smi range. Otherwise, it will use HeapNumber Object type.
Float64ToTagged::ConversionMode::kForceHeapNumber will always use HeapNumber Object to store the value.
Note that ValueRepresentation only relates to ValueNode::OpProperties, which means that if a ValueNode with OpProperties::kFloat64 and output value 1.0, it value representation will still be kFloat64.

To make this challenge solvable, I remove the CHECK() in Runtime_CheckNoWriteBarrierNeeded.
```diff
diff --git a/src/maglev/maglev-reducer-inl.h b/src/maglev/maglev-reducer-inl.h
index 60e26dfff1a..099893dd23c 100644
--- a/src/maglev/maglev-reducer-inl.h
+++ b/src/maglev/maglev-reducer-inl.h
@@ -531,14 +531,10 @@ ValueNode* MaglevReducer<BaseT>::GetTaggedValue(
           AddNewNodeNoInputConversion<Uint32ToNumber>({value}));
     }
     case ValueRepresentation::kFloat64: {
-      if (!IsEmptyNodeType(node_info->type()) && node_info->is_smi()) {
-        return alternative.set_tagged(
-            AddNewNodeNoInputConversion<CheckedSmiTagFloat64>({value}));
-      }
       // TODO(victorgomes): Do not tag Float64Constant on runtime.
       return alternative.set_tagged(
           AddNewNodeNoInputConversion<Float64ToTagged>(
-              {value}, Float64ToTagged::ConversionMode::kCanonicalizeSmi));
+              {value}, Float64ToTagged::ConversionMode::kForceHeapNumber));
     }
     case ValueRepresentation::kHoleyFloat64: {
       if (!IsEmptyNodeType(node_info->type()) && node_info->is_smi()) {
diff --git a/src/runtime/runtime-test.cc b/src/runtime/runtime-test.cc
index 612ae214d75..0f02119af49 100644
--- a/src/runtime/runtime-test.cc
+++ b/src/runtime/runtime-test.cc
@@ -2427,9 +2427,6 @@ RUNTIME_FUNCTION(Runtime_CheckNoWriteBarrierNeeded) {
   if (!object.IsHeapObject()) {
     return CrashUnlessFuzzing(isolate);
   }
-  auto heap_object = Cast<HeapObject>(object);
-  Tagged<Object> value = args[1];
-  CHECK(!WriteBarrier::IsRequired(heap_object, value));
   return args[0];
 #else
   UNREACHABLE();

```

### Trigger UAF
MaglevGraphBuilder::TrySpecializeStoreContextSlot() will use BuildStoreTaggedFieldNoWriteBarrier() to build a StoreTaggedFieldNoWriteBarrier IR Node when ContextCell is Smi.
ContextCell is based on the runtime feedback. If we keeps storing a value that fits into smi range(e.g. 1.0), ContextCell will be kSmi.
BuildStoreTaggedFieldNoWriteBarrier() will eventually call MaglevReducer::GetTaggedValue().

Write Barrier is a machanism to help V8 track objects position correctly after GC. If a living objects isn't tracked by write barrier, all pointers that pointing to that object won't be update after GC.

So we can generate a HeapNumber without Write Barrier by
1. choose a ValueNode which OpProperties has kFloat64.
2. Make the output of that ValueNode fits into smi range.
3. Use store operation to store the output.
```cpp
MaybeReduceResult MaglevGraphBuilder::TrySpecializeStoreContextSlot(
    ValueNode* context, int index, ValueNode* value, Node** store) {
  DCHECK_NOT_NULL(store);
  DCHECK(v8_flags.script_context_cells || v8_flags.function_context_cells);
  if (!context->Is<Constant>()) {
    *store =
        AddNewNode<StoreContextSlotWithWriteBarrier>({context, value}, index);
    return ReduceResult::Done();
  }

  if (IsEmptyNodeType(GetType(value))) {
    return EmitUnconditionalDeopt(DeoptimizeReason::kWrongValue);
  }

  compiler::ContextRef context_ref =
      context->Cast<Constant>()->ref().AsContext();
  auto maybe_value = context_ref.get(broker(), index);
  if (!maybe_value || maybe_value->IsTheHole() ||
      maybe_value->IsUndefinedContextCell()) {
    *store =
        AddNewNode<StoreContextSlotWithWriteBarrier>({context, value}, index);
    return ReduceResult::Done();
  }

  int offset = Context::OffsetOfElementAt(index);
  if (!maybe_value->IsContextCell()) {
    return BuildStoreTaggedField(context, value, offset,
                                 StoreTaggedMode::kDefault, store);
  }

  compiler::ContextCellRef slot_ref = maybe_value->AsContextCell();
  ContextCell::State state = slot_ref.state();
  switch (state) {
    case ContextCell::kConst: {
      auto constant = slot_ref.tagged_value(broker());
      if (!constant.has_value() ||
          (constant->IsString() && !constant->IsInternalizedString())) {
        *store = AddNewNode<StoreContextSlotWithWriteBarrier>({context, value},
                                                              index);
        return ReduceResult::Done();
      }
      broker()->dependencies()->DependOnContextCell(slot_ref, state);
      return BuildCheckNumericalValueOrByReference(
          value, *constant, DeoptimizeReason::kStoreToConstant);
    }
    case ContextCell::kSmi:
      RETURN_IF_ABORT(BuildCheckSmi(value));
      broker()->dependencies()->DependOnContextCell(slot_ref, state);
      return BuildStoreTaggedFieldNoWriteBarrier(
          GetConstant(slot_ref), value, offsetof(ContextCell, tagged_value_),
          StoreTaggedMode::kDefault, store);
    case ContextCell::kInt32:
      EnsureInt32(value, true);
      *store = AddNewNode<StoreInt32>(
          {GetConstant(slot_ref), value},
          static_cast<int>(offsetof(ContextCell, double_value_)));
      broker()->dependencies()->DependOnContextCell(slot_ref, state);
      return ReduceResult::Done();
    case ContextCell::kFloat64:
      RETURN_IF_ABORT(BuildCheckNumber(value));
      *store = AddNewNode<StoreFloat64>(
          {GetConstant(slot_ref), value},
          static_cast<int>(offsetof(ContextCell, double_value_)));
      broker()->dependencies()->DependOnContextCell(slot_ref, state);
      return ReduceResult::Done();
    case ContextCell::kDetached:
      return BuildStoreTaggedField(context, value, offset,
                                   StoreTaggedMode::kDefault, store);
  }
  UNREACHABLE();
}
```

I choose Float64Sqrt Node in my exploit.

After GC, the lower 32 bit address of object are predictable, so we can fake Float64 Array Object at the address of v0.
Change the element pointer of faked array v0, we can get addressOf, arbitrary read/write primitive.
Since the Heap Sandbox is disabled, we can overwrite the field in WASM object to RCE.
The heap spray part in my exploit isn't very statble, and I haven't found out a method to increase the success rate.