/**
 * Project Alfred - Guided Tour Component
 * Context-aware guided tours for key features
 */

import React from 'react';
import Joyride, { STATUS } from 'react-joyride';
import type { CallBackProps } from 'react-joyride';

// Custom Step interface to avoid type conflicts with React 19
interface TourStep {
  target: string;
  content: string;
  placement?: 'top' | 'bottom' | 'left' | 'right' | 'center' | 'auto';
  disableBeacon?: boolean;
}

interface GuidedTourProps {
  tourId: string;
  steps: TourStep[];
  onComplete: () => void;
}

export const GuidedTour: React.FC<GuidedTourProps> = ({ tourId, steps, onComplete }) => {
  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status } = data;
    
    if ([STATUS.FINISHED, STATUS.SKIPPED].includes(status as any)) {
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
      steps={steps as any}
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
        disableBeacon: true,
      },
      {
        target: '.conversation-input',
        content: 'This is where you chat with Alfred. Just type your message and press Enter.',
        disableBeacon: true,
      },
      {
        target: '.conversation-list',
        content: 'All your conversations are saved here. You can switch between them anytime.',
        disableBeacon: true,
      },
      {
        target: '.sidebar',
        content: 'Use the sidebar to create new conversations, access settings, and more.',
        disableBeacon: true,
      },
    ] as TourStep[],
  },
  webSearch: {
    id: 'web-search',
    steps: [
      {
        target: '.tool-web-search',
        content: 'Alfred can search the web for you! Just ask a question that requires current information.',
        disableBeacon: true,
      },
    ] as TourStep[],
  },
};
