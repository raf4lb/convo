import { useEffect, useMemo, useRef } from "react";

interface Position {
  top: number;
  left: number;
}

export function useListAnimation<T extends { id: string }>(items: T[], enabled: boolean = true) {
  const positionsRef = useRef<Map<string, Position>>(new Map());
  const containerRef = useRef<HTMLDivElement>(null);

  // Create stable dependency based on item order
  const itemIds = useMemo(() => items.map((i) => i.id).join(","), [items]);

  // Helper: Capture positions of all conversation elements
  const capturePositions = (container: HTMLDivElement): Map<string, Position> => {
    const elements = container.querySelectorAll("[data-conversation-id]");
    const positions = new Map<string, Position>();

    elements.forEach((el) => {
      const id = el.getAttribute("data-conversation-id");
      if (id) {
        const rect = el.getBoundingClientRect();
        positions.set(id, {
          top: rect.top,
          left: rect.left,
        });
      }
    });

    return positions;
  };

  useEffect(() => {
    if (!containerRef.current || !enabled) return;

    const container = containerRef.current;

    // Use RAF to ensure layout has settled before measuring
    const rafId = requestAnimationFrame(() => {
      // If we have no stored positions, this is the first render - just capture
      if (positionsRef.current.size === 0) {
        positionsRef.current = capturePositions(container);
        return;
      }

      // Capture old positions before React updates
      const oldPositions = positionsRef.current;

      // Capture new positions after React update
      const newPositions = capturePositions(container);

      // Start animations for items that moved
      const animations: Animation[] = [];

      newPositions.forEach((newPos, id) => {
        const oldPos = oldPositions.get(id);
        if (!oldPos) return; // New item, don't animate

        const deltaY = oldPos.top - newPos.top;
        const deltaX = oldPos.left - newPos.left;

        // Only animate if position changed significantly
        if (Math.abs(deltaY) > 1 || Math.abs(deltaX) > 1) {
          const element = container.querySelector(`[data-conversation-id="${id}"]`);
          if (element) {
            const animation = element.animate(
              [
                { transform: `translate(${deltaX}px, ${deltaY}px)` },
                { transform: "translate(0, 0)" },
              ],
              {
                duration: 300,
                easing: "ease-out",
              },
            );
            animations.push(animation);
          }
        }
      });

      // Update stored positions
      positionsRef.current = newPositions;

      // Cleanup: Remove positions for items no longer in the DOM
      const currentIds = new Set(items.map((item) => item.id));
      Array.from(positionsRef.current.keys()).forEach((id) => {
        if (!currentIds.has(id)) {
          positionsRef.current.delete(id);
        }
      });
    });

    // Cleanup
    return () => {
      cancelAnimationFrame(rafId);
    };
  }, [itemIds, enabled, items]); // Note: items needed for cleanup logic

  return containerRef;
}
