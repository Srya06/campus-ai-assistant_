# UI/UX Design Guidelines
## Campus AI Assistant — Student-Centric Academic Navigator & Advisory System

- **Version**: 1.0.0
- **Aesthetic**: University Academic Portal / Clean Indigo & Slate Glassmorphism

---

## 1. Visual Design Principles & Tone

1. **Student-Centric Clarity**: Academic deadlines, lab rooms, and prerequisites must be instantly legible without visual clutter.
2. **Calm & Professional Palette**: Deep navy/indigo primary paired with crisp slate neutrals, avoiding aggressive neo-brutalist styling.
3. **Explicit Information Provenance**: AI answers clearly display badge indicators:
   - `🟢 Live Gemini AI`: Sourced with LLM reasoning.
   - `⚡ Grounded Campus Knowledge`: Verified institutional data.
   - `ℹ️ Local Fallback Mode`: Deterministic offline retrieval.
4. **Accessible by Default**: High contrast ratios (WCAG AA), accessible focus rings, and legible typography.

---

## 2. Design Tokens & Color Palette

### 2.1 Color Tokens
```css
--primary: #4f46e5;         /* Deep Indigo */
--primary-hover: #4338ca;   /* Darker Indigo */
--primary-light: #eef2ff;   /* Soft Indigo Surface */
--secondary: #06b6d4;       /* Cyan Accent */
--text-main: #0f172a;       /* Slate 900 */
--text-muted: #64748b;      /* Slate 500 */
--bg-page: #f8fafc;         /* Slate 50 */
--bg-card: #ffffff;         /* Pure White */
--border: #e2e8f0;          /* Slate 200 */
--success: #10b981;         /* Emerald Green */
--warning: #f59e0b;         /* Amber Warning */
--danger: #ef4444;          /* Crimson Danger */
```

### 2.2 Typography
- **Primary Font Family**: `'Plus Jakarta Sans', system-ui, -apple-system, sans-serif`
- **Monospace Font Family**: `'JetBrains Mono', 'Fira Code', monospace` (Used for course codes, dates, time tags, room badges).
- **Scale**:
  - Hero Header: `1.55rem` (700/800 weight)
  - Section Title: `1.25rem` (700 weight)
  - Body Text: `0.95rem` (400/500 weight, line height 1.6)
  - Microcopy / Tags: `0.82rem` (600 weight)

---

## 3. Responsive Breakpoints

| Breakpoint | Width | Navigation Mode | Layout Behavior |
|---|---|---|---|
| **Mobile** | `< 768px` | Horizontal Scroll Tabs | Stacked single-column cards, full-width inputs |
| **Tablet** | `768px - 1024px` | Wrapped Pill Tabs | 2-column card grid, collapsible filters |
| **Desktop** | `> 1024px` | Fixed Top Tabs / Sidebar | Multi-column grid, persistent panels |

---

## 4. Component Standards

### 4.1 Conversational Chat
- **User Bubble**: Right-aligned, indigo background (`#4f46e5`), white text, rounded corners (`14px`), user avatar.
- **Assistant Bubble**: Left-aligned, white card background, subtle shadow, robot avatar, structured markdown parser rendering tables, lists, and bold text.
- **Citation Badges**: Clickable pills below the response linking to corresponding course codes or exam notice IDs.

### 4.2 Timetable Grid
- Day-based cards with primary headers.
- Tabular format: `Time Slot` (monospace pill) | `Subject & Code` | `Faculty` | `Venue/Lab` (colored badge).

### 4.3 Prerequisite Visual Graph
- Tree layout with directed arrows: `Course A -> Course B`.
- Strict prerequisites highlighted in Amber (`#b45309`), Co-requisites in Sky Blue (`#0369a1`).
