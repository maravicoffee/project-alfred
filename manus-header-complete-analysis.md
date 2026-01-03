# Complete Manus Header Analysis

## Frame 015 - No Preview (Sidebar Expanded)

**Header Structure:**
- Left side: Folder icon + "Manus 1.6" dropdown
- Right side (in order):
  1. Collaborate icon (people with "2")
  2. "Share" button
  3. Export/download icon
  4. Three dots menu (...)

**Key Observations:**
- Header is ABOVE the conversation content
- Header spans the full width of the content area (after sidebar)
- NO "Preview" button visible when preview is closed
- Clean, minimal header with essential buttons

## Frame 001 - Preview Open (Sidebar Collapsed)

**Header Structure:**
- Left side: Folder icon + "Manus 1.6" dropdown
- Center/Right side (in order):
  1. Collaborate icon
  2. Link icon
  3. Copy icon  
  4. Three dots (...)
  5. **"Preview" button** (highlighted/active)
  6. Code brackets icon
  7. Clock icon
  8. List icon
  9. Lock icon
  10. Settings icon
  11. Three dots (...)
  12. GitHub icon
  13. "Share" button
  14. "Published" button
  15. **X button** (to close preview)

**Key Observations:**
- When preview opens, MANY more buttons appear in the header
- The "Preview" button becomes visible and highlighted
- X button appears on the far right to close preview
- Header still spans full width but now shows preview-related controls

## Frame 030 (header-study) - Preview Open (Sidebar Collapsed)

**Header Structure:**
- Same as Frame 001
- Confirms the pattern: Preview button + all preview controls + X button

**Critical Insights:**

### 1. Header is NOT Split
- There is ONE header bar that spans the entire width
- It's not "conversation header" + "preview header"
- It's a single unified header that changes content based on state

### 2. Button Visibility Changes
**Preview Closed:**
- Folder + Title
- Collaborate (2)
- Share
- Export
- Three dots

**Preview Open:**
- Folder + Title
- Collaborate
- Link, Copy, Three dots
- **Preview button (highlighted)**
- Code, Clock, List, Lock, Settings, Three dots
- GitHub
- Share
- Published
- **X button**

### 3. Layout Behavior
- Header is positioned ABOVE both content and preview areas
- When preview opens, it slides in BELOW the header
- The header doesn't split - it expands to show more buttons
- The X button is part of the header, not the preview panel

## Implementation Requirements

### Structure:
```
┌────────────────────────────────────────────────────────────────┐
│ [Sidebar] [Single Header Bar - spans full width]               │
│           [Buttons change based on preview state]              │
├───────────┼──────────────────────┬─────────────────────────────┤
│           │                      │                             │
│ [Sidebar] │ [Content Area]       │ [Preview Area if visible]   │
│           │                      │                             │
└───────────┴──────────────────────┴─────────────────────────────┘
```

### Header States:

**State 1: Preview Closed**
- Show: Folder, Title, Collaborate, Share, Export, Menu
- Hide: Preview button, preview controls, X button

**State 2: Preview Open**
- Show: ALL buttons including Preview (highlighted), preview controls, X
- Preview button acts as indicator that preview is open
- X button closes the preview

### Key Differences from Current Implementation:

1. **Button Set Changes**: Not just adding an X - the entire button set changes
2. **Preview Button**: Should be visible when preview is OPEN (highlighted), not when closed
3. **Many More Buttons**: Code, Clock, List, Lock, Settings, GitHub, etc.
4. **Single Unified Header**: Not separate headers for each panel

## Action Items:

1. Update SharedHeader component to have two complete button sets
2. Switch between button sets based on isPreviewVisible state
3. Add all the missing buttons (Code, Clock, List, Lock, Settings, GitHub, etc.)
4. Make Preview button highlighted when preview is open
5. Ensure X button is on far right when preview is open
6. Remove any notion of separate headers for panels
