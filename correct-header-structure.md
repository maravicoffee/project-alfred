# Correct Header Structure from Manus Analysis

## Key Observation from Video Frames

### Frame 10 (No Preview):
- **Header**: Single header bar with "Manus 1.6" and buttons (Share, etc.) on the right
- **Content**: Full-width conversation content below header
- **Sidebar**: Collapsed to icons only

### Frame 30 (Preview Open):
- **Header**: SAME header bar, but now has "Preview" button highlighted and an **X button on far right**
- **Content Area Split**:
  - Left: Conversation content (narrower)
  - Right: Preview content showing SPOT website
- **Key Insight**: The header SPANS ACROSS BOTH content and preview areas
- **Preview has NO separate header** - it's just content that slides in under the shared header

## Correct Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ [Sidebar] [Shared Header spanning full width with buttons]      │
│           [When preview open: X button appears on far right]    │
├───────────┼──────────────────────┬──────────────────────────────┤
│           │                      │                              │
│ [Sidebar] │ [Main Content]       │ [Preview Content]            │
│           │                      │ (only when preview open)     │
│           │                      │                              │
└───────────┴──────────────────────┴──────────────────────────────┘
```

## What Needs to Change

### Current (Wrong):
- ConversationPanel has its own header
- PreviewPanel has its own header with all buttons
- Two separate headers side by side

### Correct (Needed):
- ONE shared header that spans across both panels
- Header contains: Title, Preview button, Share, Published, etc.
- When preview opens: X button appears in header to close it
- Preview panel is JUST content, no header
- Main content panel is JUST content, header is above it

## Implementation Plan

1. Move header OUT of ConversationPanel component
2. Create a shared Header component in App.tsx
3. Header should span the full width (after sidebar)
4. Header shows different buttons based on state (preview open/closed)
5. ConversationPanel becomes just the content area
6. PreviewPanel becomes just the content area (no header)
