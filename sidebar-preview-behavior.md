# Correct Sidebar/Preview Interaction Behavior

## Analysis from Manus Video

Comparing frame_001.png and frame_005.png from the Manus interface:

### Frame 1 (Sidebar Collapsed):
- **Sidebar**: Icon-only, narrow (~60px)
- **Main Content**: Full width conversation area
- **Preview Panel**: Full width preview panel (~750px) showing "Loading preview, please wait..."

### Frame 5 (Sidebar Expanded):
- **Sidebar**: Expanded with labels visible (~256px)
- **Main Content**: SAME width as before (not squeezed!)
- **Preview Panel**: SAME width as before (not affected in this case because there's enough space)

## Key Insight

Looking at both frames, the main content area maintains its width. The layout uses a **fixed-width main content** approach, not flex-1.

## Correct Layout Behavior

**When sidebar expands:**
- Sidebar: 60px → 256px (gains ~196px)
- Main content: Stays at fixed width (e.g., 600-800px)
- Preview panel: Absorbs the space loss, shrinks by ~196px OR gets hidden if not enough space

**When sidebar collapses:**
- Sidebar: 256px → 60px (loses ~196px)
- Main content: Stays at fixed width
- Preview panel: Gains the extra ~196px of space

## Current (Wrong) Implementation

```tsx
<Sidebar className="w-16 or w-64" />
<MainContent className="flex-1" />  ← WRONG! This makes it flexible
<Preview className="w-96" />
```

## Correct Implementation

```tsx
<Sidebar className="w-16 or w-64" />
<MainContent className="w-[600px] or w-[800px]" />  ← Fixed width!
<Preview className="flex-1 min-w-[300px]" />  ← Flexible, absorbs space changes
```

Or use a more sophisticated approach:
- Main content: `flex-1 max-w-[800px]` (flexible but capped)
- Preview: `flex-1 min-w-[300px]` (flexible, takes remaining space)

This way, when sidebar expands/collapses, the main content stays relatively stable and the preview panel adjusts.
