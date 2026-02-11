import { useCallback, useEffect, useRef, useState } from 'react';

const NEAR_BOTTOM_THRESHOLD = 100; // pixels
const THROTTLE_MS = 100;

interface UseScrollToBottomReturn {
  scrollRef: React.RefObject<HTMLDivElement>;
  scrollToBottom: (behavior?: ScrollBehavior) => void;
  isNearBottom: boolean;
}

export function useScrollToBottom(): UseScrollToBottomReturn {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [isNearBottom, setIsNearBottom] = useState(true);
  const lastCheckTime = useRef(0);

  const checkIfNearBottom = useCallback(() => {
    const now = Date.now();
    if (now - lastCheckTime.current < THROTTLE_MS) {
      return;
    }
    lastCheckTime.current = now;

    const element = scrollRef.current;
    if (!element) {
      return;
    }

    const { scrollTop, scrollHeight, clientHeight } = element;
    const distanceFromBottom = scrollHeight - scrollTop - clientHeight;
    setIsNearBottom(distanceFromBottom <= NEAR_BOTTOM_THRESHOLD);
  }, []);

  const scrollToBottom = useCallback((behavior: ScrollBehavior = 'auto') => {
    const element = scrollRef.current;
    if (!element) {
      return;
    }

    element.scrollTo({
      top: element.scrollHeight,
      behavior,
    });
  }, []);

  useEffect(() => {
    const element = scrollRef.current;
    if (!element) {
      return;
    }

    const handleScroll = () => {
      checkIfNearBottom();
    };

    element.addEventListener('scroll', handleScroll, { passive: true });

    // Initial check
    checkIfNearBottom();

    return () => {
      element.removeEventListener('scroll', handleScroll);
    };
  }, [checkIfNearBottom]);

  return {
    scrollRef,
    scrollToBottom,
    isNearBottom,
  };
}
