-- Migration: Add read column to messages table
-- Date: 2026-02-11
-- Description: Adds read boolean field to track message read status

ALTER TABLE messages
ADD COLUMN IF NOT EXISTS read BOOLEAN NOT NULL DEFAULT FALSE;
