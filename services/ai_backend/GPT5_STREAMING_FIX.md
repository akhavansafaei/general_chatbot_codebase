# GPT-5 Streaming Fix - Issue Resolution

## Problem

GPT-5 family models (gpt-5, gpt-5.1, gpt-5-mini, gpt-5-nano) were not streaming responses token-by-token like other models (GPT-4, Gemini). Instead, all text appeared at once after the complete response was generated.

## Root Cause

The OpenAI Responses API (used by GPT-5 models) uses a **completely different event structure** than the Chat Completions API (used by GPT-4):

### Chat Completions API (GPT-4)
```python
for chunk in stream:
    text = chunk.choices[0].delta.content  # Simple, direct access
    yield text
```

### Responses API (GPT-5) - THE PROBLEM
The Responses API uses **typed event objects** with semantic event types:

```python
# WRONG APPROACH (what we had):
for event in stream:
    if hasattr(event, 'delta') and hasattr(event.delta, 'text'):
        text = event.delta.text  # ❌ This doesn't exist!
        yield text
```

The issue was that we were looking for `event.delta.text`, but in the Responses API:
1. Events are typed objects (e.g., `ResponseTextDeltaEvent`)
2. Events have a `type` attribute (e.g., `"response.output_text.delta"`)
3. **The delta is a string directly**, not an object with a `.text` field
4. You need to check `event.type` to identify text delta events

## The Fix

### Correct Approach
```python
for event in stream:
    # Check event type for text delta events
    if hasattr(event, 'type') and 'text.delta' in str(event.type):
        # For ResponseTextDeltaEvent, the delta is a STRING directly
        if hasattr(event, 'delta') and event.delta is not None:
            text_chunk = event.delta  # ✓ Correct!
            yield text_chunk
```

### Key Changes in `openai_provider.py`

**Before (lines 213-237):**
```python
# Used elif statements and looked for event.delta.text
if hasattr(event, 'delta'):
    if hasattr(event.delta, 'text') and event.delta.text is not None:
        text_chunk = event.delta.text  # ❌ Never found
elif hasattr(event, 'text'):
    # ... never reached
```

**After (lines 213-244):**
```python
# Check event type first, then access event.delta as a string
if hasattr(event, 'type') and 'text.delta' in str(event.type):
    # For ResponseTextDeltaEvent, the delta is a string directly
    if hasattr(event, 'delta') and event.delta is not None:
        text_chunk = event.delta  # ✓ Correct!

# Multiple fallback checks for different event formats
if text_chunk is None and hasattr(event, 'delta'):
    if hasattr(event.delta, 'text'):
        text_chunk = event.delta.text
# ... more fallbacks
```

## Event Types in Responses API

The Responses API emits several event types during streaming:

1. `response.created` - Session started
2. `response.in_progress` - Processing
3. `response.output_item.added` - Output item started
4. `response.content_part.added` - Content part added
5. **`response.output_text.delta`** - ✓ TEXT CHUNK HERE (ResponseTextDeltaEvent)
6. `response.output_text.done` - Text complete
7. `response.done` - Response complete

Only events with type containing `"text.delta"` contain actual text chunks.

## Testing the Fix

### Debug Script
Run `python debug_gpt5_streaming.py` to see:
- Event types for first 10 events
- Delta structure and content
- Which events contain text
- Statistics on events with/without text

### Test Script
Run `python test_streaming_fix.py` to verify:
- Token-by-token streaming is working
- Chunk count is high (>5 chunks)
- Chunk sizes are small (good granularity)
- Streaming duration is >100ms (chunks spread over time)

### Expected Output (After Fix)
```
Total chunks received: 15+  (was 1)
Average chunk size: <5 characters  (was 20+)
Streaming duration: 200+ms  (was 0ms)
```

## Files Modified

1. **`src/providers/openai_provider.py`** (lines 213-244)
   - Added event type checking
   - Correctly access `event.delta` as a string
   - Multiple fallback formats for robustness

2. **`debug_gpt5_streaming.py`**
   - Added event type inspection
   - Check if delta is a string
   - Uses same logic as provider

3. **`test_streaming_fix.py`** (new file)
   - Comprehensive streaming quality tests
   - Metrics for chunk count, size, timing
   - Comparison with GPT-4

## Technical Details

### OpenAI Responses API Event Structure
```python
class ResponseTextDeltaEvent:
    type: str = "response.output_text.delta"
    delta: str  # ← The text chunk is here (string, not object)
    # ... other fields
```

### Why This Matters
- **GPT-5 models use Responses API** (not Chat Completions)
- **Responses API uses typed events** with semantic types
- **Delta is a string**, not an object with `.text`
- **Event type indicates content** (must check `event.type`)

## Migration Notes

This fix ensures GPT-5 models stream responses token-by-token, matching the behavior of:
- GPT-4 and GPT-3.5 (Chat Completions API)
- Gemini models (Google Generative AI API)
- Anthropic Claude (Messages API)

All models now provide a consistent streaming experience!
