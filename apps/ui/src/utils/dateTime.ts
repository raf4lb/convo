/**
 * Formats an ISO timestamp string to HH:MM using the browser's local timezone.
 *
 * @param timestamp - ISO 8601 timestamp string (e.g., "2024-02-11T14:30:45+00:00")
 * @returns Formatted time string (e.g., "14:30")
 */
export function formatMessageTime(timestamp: string): string {
  try {
    const date = new Date(timestamp);
    return date.toLocaleTimeString("pt-BR", {
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch (error) {
    console.error("Failed to format timestamp:", timestamp, error);
    return timestamp; // Fallback to raw timestamp
  }
}

/**
 * Formats a date to relative time display (e.g., "Ontem", "2 dias atrás").
 * Used for conversation list timestamps.
 *
 * @param date - Date object or ISO string
 * @returns Formatted relative time string
 */
export function formatRelativeTime(date: Date | string): string {
  const dateObj = typeof date === "string" ? new Date(date) : date;
  const now = new Date();
  const diffInDays = Math.floor(
    (now.getTime() - dateObj.getTime()) / (1000 * 60 * 60 * 24)
  );

  if (diffInDays === 0) {
    // Today: show time only (HH:MM)
    return dateObj.toLocaleTimeString("pt-BR", {
      hour: "2-digit",
      minute: "2-digit",
    });
  } else if (diffInDays === 1) {
    // Yesterday
    return "Ontem";
  } else if (diffInDays < 7) {
    // This week
    return `${diffInDays} dias atrás`;
  } else {
    // Older: show date (DD/MM)
    return dateObj.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
    });
  }
}
