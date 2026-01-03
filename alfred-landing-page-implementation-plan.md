# Alfred Landing Page - Implementation Plan

## What I Understood from the Video

Based on my analysis of the Manus landing page video, here's what I observed and how it works:

### 1. Landing Page vs Task View

**Landing Page (What we need to create):**
- Shows when user first visits or clicks "New task"
- Large centered prompt: "What can I do for you?"
- Big input box for starting a task
- Quick action buttons below input
- Feature showcase carousel at bottom
- Simpler header (no Preview/Share/Published buttons)

**Task View (What we already have):**
- Shows when user is in an active conversation
- Chat messages displayed
- Input at bottom
- Full header with Preview, Share, Published buttons
- Can toggle preview panel

### 2. Sidebar Behavior (Same in Both Views)

The sidebar remains consistent across both landing and task views:

**Top Section:**
- "New task" button (primary/highlighted)
- "Search" button
- "Library" button

**Projects Section:**
- "Projects" header with "+" to add new
- Scrollable list of project folders
- Each project is clickable

**All Tasks Section:**
- "All tasks" header with filter icon
- List of tasks with status indicators (colored dots)
- Scrollable list

**Bottom Section:**
- Promotional card ("Share Manus with a friend")
- Footer icons: Settings, Help, Mobile, Desktop

### 3. Header Behavior (Different Between Views)

**Landing Page Header:**
- Left: Logo + "Alfred 1.0" dropdown
- Right: Notifications bell, Credits counter, User avatar
- NO task-specific buttons (Preview, Share, Published)

**Task View Header:**
- Same left side
- Right: All the buttons we implemented (Preview, Share, Published, etc.)
- Changes based on preview state

### 4. Interactive Elements

**Credits Counter:**
- Clicking opens popup showing credit breakdown
- Shows total, free, monthly credits
- Daily refresh information
- "Add credits" and "View usage" buttons

**Help Icon:**
- Opens documentation page
- Separate view with navigation

**Quick Action Buttons:**
- "Create slides" - Starts slide creation task
- "Build website" - Starts website building task
- "Develop apps" - Starts app development task
- "Design" - Starts design task
- "More" - Shows additional options

**Feature Carousel:**
- Shows promotional cards for features
- Swipeable/clickable
- Pagination dots show position

### 5. Input Box Features

**Large centered input on landing page:**
- Placeholder: "Assign a task or ask anything"
- "+" button on left (attachments?)
- Tool integration icons (GitHub, Google Drive, Google, +2)
- Voice input icon
- Send button
- When user types and sends, transitions to task view

## Implementation Approach

### Option 1: Separate Routes (Recommended)

Create two distinct routes:
- `/` or `/home` - Landing page
- `/task/:id` - Task conversation view

**Pros:**
- Clean separation of concerns
- Different headers for different contexts
- Easy to maintain
- Proper URL structure

**Cons:**
- Need routing setup
- Need to handle navigation between views

### Option 2: Conditional Rendering

Keep single route, show landing page when no task is active:

**Pros:**
- Simpler routing
- Already partially implemented

**Cons:**
- More complex conditional logic
- Header needs to handle multiple states
- Harder to maintain

### Recommended: Option 1 with React Router

## Implementation Steps

### Phase 1: Setup Routing
1. Install React Router
2. Create route structure:
   - `/` → LandingPage component
   - `/task/:id` → TaskView component
3. Update App.tsx to use router

### Phase 2: Create Landing Page Component
1. Create `LandingPage.tsx` with:
   - Hero section with "What can I do for you?"
   - Large centered input box
   - Quick action buttons
   - Feature carousel
2. Use simpler header (no task-specific buttons)
3. Handle input submission → navigate to new task

### Phase 3: Update Task View
1. Rename current conversation view to `TaskView.tsx`
2. Keep existing header with all buttons
3. Keep preview panel functionality
4. Handle task ID from URL params

### Phase 4: Update Sidebar
1. Make sidebar work across both views
2. "New task" button → navigate to landing page
3. Clicking a task → navigate to that task view
4. Keep all existing functionality

### Phase 5: Implement Interactive Features
1. Credits popup component
2. Help/documentation link
3. Quick action handlers
4. Feature carousel component

## File Structure

```
frontend/src/
├── App.tsx (Router setup)
├── pages/
│   ├── LandingPage.tsx (New)
│   └── TaskView.tsx (Refactored from current)
├── components/
│   ├── Sidebar.tsx (Shared)
│   ├── SharedHeader.tsx (Needs variant prop)
│   ├── ConversationPanel.tsx (For task view)
│   ├── PreviewPanel.tsx (For task view)
│   ├── LandingHero.tsx (New)
│   ├── QuickActions.tsx (New)
│   ├── FeatureCarousel.tsx (New)
│   └── CreditsPopup.tsx (New)
```

## Questions for Confirmation

1. **Routing**: Should we use React Router for separate routes, or conditional rendering?
2. **Credits System**: Do we need a real credits system, or just UI mockup for now?
3. **Quick Actions**: Should these actually trigger specific task types, or just populate the input?
4. **Feature Carousel**: What features should we showcase for Alfred?
5. **Documentation**: Do we need a separate docs page like Manus, or just link externally?

## What We Keep from Current Implementation

✅ Sidebar component (works in both views)
✅ SharedHeader component (add variant for landing vs task)
✅ ConversationPanel (for task view)
✅ PreviewPanel (for task view)
✅ OpenAI integration (for task conversations)
✅ Mobile viewport fixes (100dvh)
✅ Color scheme (Deep Forest green)

## What We Add

🆕 Landing page route and component
🆕 Large hero input section
🆕 Quick action buttons
🆕 Feature carousel
🆕 Credits popup
🆕 Header variant for landing page
🆕 Navigation between landing and task views

## Summary

The landing page is essentially a **welcome/starting point** that transitions to the task view once the user starts a conversation. The sidebar and overall layout structure remain the same, but the main content area and header buttons change based on context.

Does this understanding match what you had in mind? Should I proceed with implementing this as separate routes with React Router?
