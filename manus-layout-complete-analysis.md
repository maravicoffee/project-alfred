# Complete Manus Layout Analysis from Video

## Key States Observed

### State 1: Sidebar Collapsed, No Preview (Frame 30)
- **Sidebar**: ~60px (icon-only, collapsed)
- **Main Content**: Takes FULL remaining width (~1220px)
- **Preview**: Hidden/Not visible
- **Behavior**: Main content expands to fill all available space when no preview

### State 2: Sidebar Expanded, No Preview (Frame 10, 15, 35)
- **Sidebar**: ~340px (expanded with full labels and project list)
- **Main Content**: Takes FULL remaining width (~940px)
- **Preview**: Hidden/Not visible
- **Behavior**: Main content still takes all available space, just less total space available

### State 3: Sidebar Collapsed, Preview Open (Frame 1, 5)
- **Sidebar**: ~60px (icon-only)
- **Main Content**: ~500px (about 40% of available space)
- **Preview**: ~720px (about 60% of available space)
- **Total available**: 1220px
- **Behavior**: Content and preview share the available space

### State 4: Sidebar Expanded, Preview Open (Frame 10 with preview)
- **Sidebar**: ~340px (expanded)
- **Main Content**: ~470px (about 50% of available space)
- **Preview**: ~470px (about 50% of available space)
- **Total available**: 940px
- **Behavior**: Content and preview split remaining space roughly 50/50

## Critical Insights

### 1. **WITHOUT Preview Open:**
   - Main content is `flex-1` and takes ALL available space
   - Sidebar changes don't affect main content's flex behavior
   - Main content just has more or less total space available

### 2. **WITH Preview Open:**
   - Main content and Preview BOTH are flexible
   - They share the available space (after sidebar)
   - When sidebar collapses: Extra space is distributed between BOTH main and preview
   - When sidebar expands: Both main and preview shrink proportionally

### 3. **The Key Difference:**
   - Preview is NOT always visible
   - When preview is HIDDEN: Main content takes full width
   - When preview is VISIBLE: Main content and preview share space

## Correct Implementation

```tsx
<div className="flex">
  {/* Sidebar - Fixed width, changes between collapsed/expanded */}
  <Sidebar className={collapsed ? "w-16" : "w-[340px]"} />
  
  {/* Main Content - Always flex-1, but behavior changes based on preview */}
  <MainContent className="flex-1 min-w-[400px]" />
  
  {/* Preview - Only rendered when visible, also flex-1 */}
  {isPreviewVisible && (
    <Preview className="flex-1 min-w-[400px]" />
  )}
</div>
```

### Why This Works:

1. **No Preview**: Main content is the only flex-1 element, takes all space
2. **With Preview**: BOTH are flex-1, so they share space equally
3. **Sidebar changes**: Affect total available space, both flex elements adjust proportionally

## What Was Wrong Before

I was trying to use `max-w-[600px]` on main content, which prevented it from taking full width when preview was hidden. The solution is:

- Main content should be `flex-1` WITHOUT max-width restrictions
- Preview should also be `flex-1` when visible
- Both should have reasonable min-widths to prevent collapsing too small
- The flex system naturally handles the space distribution

## Mobile Considerations

On mobile (narrow viewports), when both panels would be too cramped:
- Could hide preview automatically
- Or stack vertically
- Or use tabs/overlay approach

But the core desktop behavior is: **both panels are flex-1 and share space equally when preview is open**.
