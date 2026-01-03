# Mobile Viewport Issue Diagnosis

## Video Evidence Analysis

From the video frames captured from the user's mobile device (HUAWEI Mate XT):

### Frame 1-3: Initial State
- URL bar visible at top
- Icon sidebar showing on left
- Conversation list panel visible
- Main chat area shows "Start a conversation with Alfred" and "Ask me anything!"
- **CRITICAL: Chat input field is NOT visible** - it's below the viewport
- User has to scroll down to see the input field

### Frame 5: After Scrolling Down
- URL bar has been hidden (mobile browser behavior when scrolling)
- Chat input field NOW visible at bottom: "Send message to Alfred"
- User profile icon appears in bottom left corner
- This proves the input field exists but is positioned below the initial viewport

### Frame 7: Scrolled Back Up
- URL bar visible again
- Input field hidden again below viewport
- Back to initial state

## Root Cause Analysis

The issue is **MOBILE-SPECIFIC** and related to:

1. **Mobile browser chrome** - The URL bar, navigation controls, and system UI take up significant vertical space on mobile
2. **100vh problem** - CSS `h-screen` (which translates to `height: 100vh`) doesn't account for mobile browser UI
3. **Mobile viewport height** - On mobile, `100vh` includes the browser chrome area, but the actual visible area is smaller

When the URL bar is visible, the actual viewport is smaller than 100vh, causing the bottom content (chat input) to be pushed below the visible area.

## The Classic Mobile Viewport Bug

This is a well-known issue in mobile web development:
- Desktop: `100vh` = actual viewport height ✅
- Mobile: `100vh` = viewport height INCLUDING browser chrome ❌
- Result: Content at bottom gets cut off when browser UI is visible

## Solution Required

Need to use one of these approaches:
1. Use `height: 100dvh` (dynamic viewport height) - modern CSS solution
2. Use `height: 100svh` (small viewport height) - accounts for maximum browser UI
3. Use JavaScript to calculate actual viewport height
4. Use `position: fixed` for the input field to keep it always visible
5. Adjust layout to use `min-height` instead of fixed `height`

The best solution is to use `100dvh` or `100svh` for mobile devices, which properly accounts for browser UI.
