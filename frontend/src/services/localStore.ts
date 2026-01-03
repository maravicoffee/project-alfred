/**
 * Project Alfred - Local Storage Service
 * Handles all local storage operations for anonymous users
 */

export interface LocalConversation {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
}

export interface LocalMessage {
  id: string;
  conversationId: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  createdAt: string;
}

export interface LocalUserState {
  isAnonymous: boolean;
  interactionCount: number;
  firstVisit: string;
  lastVisit: string;
}

const STORAGE_KEYS = {
  CONVERSATIONS: 'alfred_conversations',
  MESSAGES: 'alfred_messages',
  USER_STATE: 'alfred_user_state',
  CURRENT_CONVERSATION: 'alfred_current_conversation'
};

class LocalStorageService {
  // User State Management
  getUserState(): LocalUserState {
    const stored = localStorage.getItem(STORAGE_KEYS.USER_STATE);
    if (stored) {
      return JSON.parse(stored);
    }
    
    // Initialize new user state
    const newState: LocalUserState = {
      isAnonymous: true,
      interactionCount: 0,
      firstVisit: new Date().toISOString(),
      lastVisit: new Date().toISOString()
    };
    
    this.saveUserState(newState);
    return newState;
  }
  
  saveUserState(state: LocalUserState): void {
    localStorage.setItem(STORAGE_KEYS.USER_STATE, JSON.stringify(state));
  }
  
  incrementInteractionCount(): number {
    const state = this.getUserState();
    state.interactionCount += 1;
    state.lastVisit = new Date().toISOString();
    this.saveUserState(state);
    return state.interactionCount;
  }
  
  // Conversation Management
  getConversations(): LocalConversation[] {
    const stored = localStorage.getItem(STORAGE_KEYS.CONVERSATIONS);
    return stored ? JSON.parse(stored) : [];
  }
  
  getConversation(id: string): LocalConversation | null {
    const conversations = this.getConversations();
    return conversations.find(c => c.id === id) || null;
  }
  
  saveConversation(conversation: LocalConversation): void {
    const conversations = this.getConversations();
    const index = conversations.findIndex(c => c.id === conversation.id);
    
    if (index >= 0) {
      conversations[index] = conversation;
    } else {
      conversations.push(conversation);
    }
    
    localStorage.setItem(STORAGE_KEYS.CONVERSATIONS, JSON.stringify(conversations));
  }
  
  createConversation(title: string): LocalConversation {
    const conversation: LocalConversation = {
      id: `local-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      title,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    this.saveConversation(conversation);
    this.setCurrentConversation(conversation.id);
    return conversation;
  }
  
  deleteConversation(id: string): void {
    const conversations = this.getConversations();
    const filtered = conversations.filter(c => c.id !== id);
    localStorage.setItem(STORAGE_KEYS.CONVERSATIONS, JSON.stringify(filtered));
    
    // Also delete all messages for this conversation
    const messages = this.getMessages(id);
    messages.forEach(m => this.deleteMessage(m.id));
  }
  
  // Message Management
  getMessages(conversationId: string): LocalMessage[] {
    const stored = localStorage.getItem(STORAGE_KEYS.MESSAGES);
    const allMessages: LocalMessage[] = stored ? JSON.parse(stored) : [];
    return allMessages.filter(m => m.conversationId === conversationId);
  }
  
  saveMessage(message: LocalMessage): void {
    const stored = localStorage.getItem(STORAGE_KEYS.MESSAGES);
    const messages: LocalMessage[] = stored ? JSON.parse(stored) : [];
    messages.push(message);
    localStorage.setItem(STORAGE_KEYS.MESSAGES, JSON.stringify(messages));
    
    // Update conversation's updatedAt
    const conversation = this.getConversation(message.conversationId);
    if (conversation) {
      conversation.updatedAt = new Date().toISOString();
      this.saveConversation(conversation);
    }
  }
  
  createMessage(conversationId: string, role: 'user' | 'assistant' | 'system', content: string): LocalMessage {
    const message: LocalMessage = {
      id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      conversationId,
      role,
      content,
      createdAt: new Date().toISOString()
    };
    
    this.saveMessage(message);
    this.incrementInteractionCount();
    return message;
  }
  
  deleteMessage(id: string): void {
    const stored = localStorage.getItem(STORAGE_KEYS.MESSAGES);
    const messages: LocalMessage[] = stored ? JSON.parse(stored) : [];
    const filtered = messages.filter(m => m.id !== id);
    localStorage.setItem(STORAGE_KEYS.MESSAGES, JSON.stringify(filtered));
  }
  
  // Current Conversation
  getCurrentConversationId(): string | null {
    return localStorage.getItem(STORAGE_KEYS.CURRENT_CONVERSATION);
  }
  
  setCurrentConversation(id: string): void {
    localStorage.setItem(STORAGE_KEYS.CURRENT_CONVERSATION, id);
  }
  
  // Migration & Cleanup
  getAllLocalData() {
    return {
      conversations: this.getConversations(),
      messages: localStorage.getItem(STORAGE_KEYS.MESSAGES) ? JSON.parse(localStorage.getItem(STORAGE_KEYS.MESSAGES)!) : [],
      userState: this.getUserState()
    };
  }
  
  clearAllLocalData(): void {
    localStorage.removeItem(STORAGE_KEYS.CONVERSATIONS);
    localStorage.removeItem(STORAGE_KEYS.MESSAGES);
    localStorage.removeItem(STORAGE_KEYS.USER_STATE);
    localStorage.removeItem(STORAGE_KEYS.CURRENT_CONVERSATION);
  }
  
  // Utility
  hasLocalData(): boolean {
    const conversations = this.getConversations();
    return conversations.length > 0;
  }
}

export const localStore = new LocalStorageService();
