# Project Alfred - Onboarding Implementation Plan

**Date:** January 3, 2026
**Author:** Manus AI

---

## 1. Overview

This document provides a detailed, sprint-by-sprint implementation plan for the Project Alfred onboarding experience. This will be the focus of the first part of **Phase 2**.

---

## 2. Sprint Breakdown

### Sprint 11: Local-First & Anonymous User Experience

**Goal:** Implement the complete anonymous user experience with local persistence.

**Tasks:**

1.  **Frontend: Local Storage Service**
    *   Create a service (`src/services/localStore.ts`) to handle all interactions with `localStorage`.
    *   Methods: `getConversations`, `saveConversation`, `getMessages`, `saveMessage`, `clearLocalData`.
2.  **Frontend: Anonymous User State**
    *   Implement a state management solution (e.g., Zustand, Redux) to track the current user state (anonymous vs. authenticated).
    *   Modify the UI to use the local storage service when the user is anonymous.
3.  **Frontend: Signup Nudge**
    *   Create a subtle, non-intrusive UI component that appears after 3-5 interactions.
    *   This component will trigger the signup modal.
4.  **Frontend: Signup/Login Modal**
    *   Build a clean, elegant modal with options for email (magic link) and Google login.
    *   The modal should be consistent with the "Deep Forest" theme.

**Acceptance Criteria:**
*   Anonymous users can have conversations, and they persist after refreshing the page.
*   The signup nudge appears at the appropriate time.
*   The signup/login modal is fully functional and visually polished.

### Sprint 12: Authentication & Data Migration

**Goal:** Implement user authentication and automatic data migration.

**Tasks:**

1.  **Backend: Supabase Auth Integration**
    *   Integrate the Supabase Python library into the backend.
    *   Create API endpoints for handling signup, login, and user sessions.
2.  **Frontend: Authentication Service**
    *   Create a service (`src/services/auth.ts`) to handle all authentication-related API calls.
    *   Implement logic for handling magic links and Google OAuth callbacks.
3.  **Backend: Data Migration Endpoint**
    *   Create a secure API endpoint that accepts local conversation data and syncs it to the user's new cloud account.
4.  **Frontend: Migration Logic**
    *   On successful signup, trigger a script that sends all local data to the migration endpoint.
    *   Once migration is complete, clear the local storage and switch to using the cloud API.

**Acceptance Criteria:**
*   Users can successfully sign up and log in.
*   Local data is automatically and correctly migrated to the cloud.
*   The application seamlessly transitions from local to cloud data storage.

### Sprint 13: Welcome Flow & Guided Tours

**Goal:** Create a welcoming experience for new users and implement contextual guidance.

**Tasks:**

1.  **Backend: Welcome Message Logic**
    *   Create a mechanism to send a personalized welcome message to new users.
2.  **Frontend: Welcome Experience**
    *   Display the welcome message in the user's conversation list.
    *   Potentially include a brief, elegant animation or visual cue to celebrate the new account.
3.  **Frontend: Guided Tour Integration**
    *   Integrate a library like `react-joyride`.
    *   Create a simple, optional tour for a key feature (e.g., using the web search tool).
4.  **Frontend: Contextual Tour Triggers**
    *   Implement logic to trigger the guided tour only when a user first encounters the relevant feature.

**Acceptance Criteria:**
*   New users receive a welcome message.
*   The guided tour for the web search tool works correctly and is not intrusive.

---

## 3. Technology Stack

| Component | Technology | Justification |
| :--- | :--- | :--- |
| **Local Storage** | `localStorage` API | Simple, built-in, and perfect for anonymous user data. |
| **Authentication** | Supabase Auth | Handles passwordless, social, and traditional auth with ease. |
| **State Management** | Zustand | Lightweight, simple, and effective for managing user state. |
| **Guided Tours** | React-Joyride | Mature, customizable, and easy to integrate with React. |

---

## 4. Timeline

Each sprint is estimated to take approximately **1-2 weeks** for our two-person team. The entire onboarding implementation should be complete within **3-6 weeks**.

---

This detailed plan provides a clear roadmap for building a world-class onboarding experience for Project Alfred. By focusing on a frictionless, value-first approach, we will set our users up for success from their very first interaction.
