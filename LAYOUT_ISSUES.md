# Layout Issues - Current State

## Issues Observed (from deployed site screenshot):

1. **Header Missing**: The "Alfred 1.0" header in the middle panel is at the very top edge, partially cut off by browser chrome
2. **Show Preview Button**: Visible in top right (elements 13, 14) but no space for it
3. **Chat Input**: At bottom (element 16) but appears to be cut off
4. **Icon Sidebar**: Present on left (elements 2-11) - GOOD
5. **Conversation List**: Present (element 12 "New Chat") - GOOD
6. **Main Chat Area**: Taking up center space - GOOD

## Root Cause:
The panels are using `h-screen` which is 100vh, but this doesn't account for:
- Browser chrome (address bar, etc.)
- The panels are positioned absolutely or the flex container isn't constrained properly

## Solution Needed:
1. Use `h-full` instead of `h-screen` on child panels
2. Ensure parent container is `h-screen overflow-hidden`
3. All child panels should be `h-full` not `h-screen`
4. Test on actual deployed site before marking as complete
