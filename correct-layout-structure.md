# Correct Manus Layout Structure

## Analysis from Real Manus Screenshot

### 3-Panel Layout (NOT 4!)

**Panel 1: Left Sidebar (Collapsible)**
- Width: ~256px expanded, ~60px collapsed
- Contains:
  - Manus logo at top
  - "New task" button
  - "Search" button
  - "Library" button
  - "Projects" section with project list
  - "All tasks" section
  - Task list items
  - Bottom actions
- Behavior: Can collapse to icon-only view

**Panel 2: Main Content Area (Single Panel with View Switching)**
- This is ONE panel that shows different views:
  - When no conversation selected: Shows conversation list
  - When conversation selected: Shows chat interface with messages and input
  - The conversation list and chat interface are NOT separate panels - they occupy the same space
- Width: Flexible, takes remaining space between sidebar and preview
- Contains:
  - Header with title (e.g., "Manus 1.6")
  - Main content (either list view or chat view)
  - Action buttons in header

**Panel 3: Right Preview Panel (Toggleable)**
- Width: ~400px when visible
- Hidden by default
- Shows when "Preview" or "Collaborate" or "Share" is clicked
- Contains: Preview content, collaboration tools, etc.

## Key Difference from Current Implementation

**Current (WRONG):**
```
[Icon Sidebar] [Conversation List] [Chat Area] [Preview]
     60px           256px            flex         384px
```

**Correct (RIGHT):**
```
[Sidebar]  [Main Content - switches between list/chat]  [Preview]
  256px                    flex                           400px
```

## Implementation Changes Needed

1. **Remove ConversationList as separate panel**
2. **Create view state in App.tsx**: 'list' | 'chat'
3. **Main content area shows**:
   - ConversationList view when no conversation selected
   - ConversationPanel view when conversation selected
4. **Sidebar should contain**:
   - Navigation items
   - Project list
   - Conversation access (maybe as a menu item)
5. **When user clicks "New Chat"**:
   - Switch main content view from 'list' to 'chat'
   - Show empty chat interface
6. **When user selects a conversation**:
   - Switch main content view to 'chat'
   - Load that conversation

This matches how Manus actually works!
