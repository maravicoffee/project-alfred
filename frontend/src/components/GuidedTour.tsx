/**
 * Project Alfred - Guided Tour Component
 * Context-aware guided tours for key features
 */

import React from 'react';
import Joyride, { Step, CallBackProps, STATUS } from 'react-joyride';

interface GuidedTourProps {
  tourId: string;
  steps: Step[];
  onComplete: () => void;
}

export const GuidedTour: React.FC<GuidedTourProps> = ({ tourId, steps, onComplete }) => {
  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status } = data;
    
    if ([STATUS.FINISHED, STATUS.SKIPPED].includes(status)) {
      // Mark tour as completed
      localStorage.setItem(`alfred_tour_${tourId}`, 'completed');
      onComplete();
    }
  };
  
  // Check if tour has been completed
  const isCompleted = localStorage.getItem(`alfred_tour_${tourId}`) === 'completed';
  
  if (isCompleted) return null;
  
  return (
    <Joyride
      steps={steps}
      continuous
      showProgress
      showSkipButton
      callback={handleJoyrideCallback}
      styles={{
        options: {
          primaryColor: '#2D5F4C',
          zIndex: 10000,
        },
        tooltip: {
          borderRadius: 8,
        },
        buttonNext: {
          backgroundColor: '#2D5F4C',
          borderRadius: 6,
        },
        buttonBack: {
          color: '#2D5F4C',
        },
      }}
    />
  );
};

// Predefined tours
export const TOURS = {
  welcome: {
    id: 'welcome',
    steps: [
      {
        target: 'body',
        content: 'Welcome to Alfred! Let me show you around.',
        placement: 'center',
      } as Step,
      {
        target: '.conversation-input',
        content: 'This is where you chat with Alfred. Just type your message and press Enter.',
      } as Step,
      {
        target: '.conversation-list',
        content: 'All your conversations are saved here. You can switch between them anytime.',
      } as Step,
      {
        target: '.sidebar',
        content: 'Use the sidebar to create new conversations, access settings, and more.',
      } as Step,
    ],
  },
  webSearch: {
    id: 'web-search',
    steps: [
      {
        target: '.tool-web-search',
        content: 'Alfred can search the web for you! Just ask a question that requires current information.',
      } as Step,
    ],
  },
};
