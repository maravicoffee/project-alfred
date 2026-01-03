/**
 * Project Alfred - Client-Side AI Service
 * Handles AI interactions using OpenAI API directly from the browser
 */

interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface ChatResponse {
  status: string;
  response: string;
  error?: string;
}

class AIService {
  private apiKey: string;
  private conversationHistory: ChatMessage[] = [];

  constructor() {
    // In production, this should be loaded from environment variables
    // For now, we'll use a placeholder that can be configured
    this.apiKey = import.meta.env.VITE_OPENAI_API_KEY || '';
    
    // Initialize with system prompt
    this.conversationHistory = [
      {
        role: 'system',
        content: `You are Alfred, an intelligent AI assistant created to help users with various tasks. 
You are proactive, thoughtful, and strategic in your approach. You analyze situations, create plans, 
and execute tasks efficiently. You bridge the gap between thought and action.

Your capabilities include:
- Answering questions and providing information
- Helping with problem-solving and decision-making
- Assisting with planning and organization
- Providing thoughtful analysis and insights

Always be helpful, clear, and concise in your responses.`
      }
    ];
  }

  /**
   * Send a message and get AI response
   */
  async chat(message: string): Promise<ChatResponse> {
    try {
      // Add user message to history
      this.conversationHistory.push({
        role: 'user',
        content: message
      });

      // For demo purposes without API key, return a mock response
      if (!this.apiKey) {
        const mockResponse = this.getMockResponse(message);
        this.conversationHistory.push({
          role: 'assistant',
          content: mockResponse
        });
        
        return {
          status: 'success',
          response: mockResponse
        };
      }

      // Call OpenAI API
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: 'gpt-4',
          messages: this.conversationHistory,
          temperature: 0.7,
          max_tokens: 1000
        })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      const assistantMessage = data.choices[0].message.content;

      // Add assistant response to history
      this.conversationHistory.push({
        role: 'assistant',
        content: assistantMessage
      });

      return {
        status: 'success',
        response: assistantMessage
      };

    } catch (error) {
      console.error('AI Service error:', error);
      return {
        status: 'error',
        response: 'I apologize, but I encountered an error processing your request. Please try again.',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get mock response for demo mode (when no API key is configured)
   */
  private getMockResponse(message: string): string {
    const lowerMessage = message.toLowerCase();

    if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
      return "Hello! I'm Alfred, your AI assistant. I'm here to help you with various tasks, answer questions, and provide insights. How can I assist you today?";
    }

    if (lowerMessage.includes('what can you do') || lowerMessage.includes('capabilities') || lowerMessage.includes('help')) {
      return `I'm Alfred, and I can help you with:

• **Information & Research**: Answer questions and provide detailed explanations
• **Problem Solving**: Help you think through challenges and find solutions
• **Planning & Organization**: Assist with task planning and project management
• **Analysis**: Provide thoughtful analysis of situations and data
• **Creative Tasks**: Help with writing, brainstorming, and creative projects

I use a cognitive loop approach: I analyze your request, create a plan, execute it, and learn from the results. What would you like help with?`;
    }

    if (lowerMessage.includes('thank')) {
      return "You're welcome! I'm always here to help. Feel free to ask me anything else!";
    }

    // Generic response
    return `I understand you're asking about "${message}". 

I'm currently running in demo mode. In the full version, I would:
1. **Analyze** your request to understand the context and requirements
2. **Plan** the best approach to address your needs
3. **Execute** the necessary steps to provide a comprehensive answer
4. **Observe** the results and refine my approach

For now, I can engage in conversation and provide general assistance. What specific topic would you like to explore?`;
  }

  /**
   * Clear conversation history
   */
  clearHistory(): void {
    this.conversationHistory = [this.conversationHistory[0]]; // Keep system prompt
  }

  /**
   * Get conversation history
   */
  getHistory(): ChatMessage[] {
    return this.conversationHistory;
  }
}

export const aiService = new AIService();
export default aiService;
