# Chrome DevTools Guide

Reflects tool behavior as of April 2026. Capabilities change; verify against the official documentation links at the bottom before modifying this guide.

Operational guide for using Claude in Chrome well. Read before starting Chrome work. The default imagination of "browser automation" (click coordinates, screenshots) maps poorly onto the tools actually available and leads to slow, heavy, error-prone sessions. This guide front-loads the approach that works.

---

## Mental Model

Chrome is devtools, not browser automation. Primary tools are JS and DOM queries, not clicks and screenshots. Reach for read_page, get_page_text, find, and javascript_tool first. Use form_input for setting form values and fall back to the React-compatible JS pattern (see Form Filling below) for fields that resist form_input or sit inside frameworks with custom handlers.

For interaction (clicking, scrolling, hovering), the computer tool accepts element refs from read_page and find. This means find → click-by-ref is a complete workflow with no screenshot needed. The ref-based path covers reading, writing, clicking, scrolling, and hovering — screenshots are only necessary when the visual layout itself is the question.

---

## Tool Reference

**read_page** — Returns the accessibility tree with element refs. Three parameters worth knowing:
- `filter`: "interactive" returns only buttons, links, and inputs. Significantly smaller output on pages with heavy non-interactive content (forms, dashboards, text-heavy articles with little navigation). Less reduction on link-heavy pages where the interactive set is already most of the content. Use this as the default when looking for actionable elements.
- `ref_id`: Scopes the tree to one element and its children. Use after find or a previous read_page to drill into a specific section without re-reading the whole page.
- `depth`: Limits tree traversal depth (default 15). Reduce if output is too large.

Output includes the current viewport dimensions. Truncates long text fields (textarea contents, article bodies). Use get_page_text or javascript_tool when you need the full text of a long field.

**get_page_text** — Extracts readable text content. Good for articles, blog posts, and text-heavy pages. Has a fixed 50000 character limit and will error on very long pages — there is no max_chars parameter (unlike read_page). When the limit is hit, use read_page with ref_id to scope to the section you need, or javascript_tool to extract specific text.

**find** — Returns element refs from a natural-language query. Query phrasing matters: "search bar" may find container elements while "search input field" finds the actual textbox. Be specific about element type when you need a particular kind of element. find also handles descriptive semantic queries about meaning, not just element type — descriptions of what a link or element represents can work as well as element-type labels.

**javascript_tool** — Swiss army knife. Read values, query the DOM, inspect state, interact with conditional UI, return structured objects. The last expression is returned (no explicit return statement — a `return` outside a function body fails loudly with a SyntaxError, so this mistake is immediately visible). See Verification Pattern below for efficient multi-read usage.

**form_input** — Sets form values by ref. Works for straightforward inputs including textareas with newlines. Reports the previous value in its response, giving built-in verification. Falls back to the JS pattern (see Form Filling) when the field resists or has framework-specific handlers.

**computer** — Mouse and keyboard interaction. Accepts a `ref` parameter as an alternative to coordinates for click, hover, and scroll_to actions. This means you can find an element by ref, then click it without a screenshot:

    find → ref_N → computer left_click ref=ref_N
    find → ref_N → computer hover ref=ref_N
    find → ref_N → computer scroll_to ref=ref_N

Also supports zoom (region screenshot for close inspection of a small area, lower cost than a full screenshot).

**file_upload** — Uploads files to file input elements. Do NOT click file inputs — clicking opens a native file picker dialog you cannot see or interact with. Instead, use read_page or find to locate the file input ref, then call file_upload with that ref and the file path(s).

**read_console_messages** — Reads browser console output (logs, errors, warnings). Useful for debugging JS errors or understanding page behavior. Tracking starts on first call, so it does not capture messages from before it was activated — if the page loaded before the first call, refresh the page to capture load-time messages. Call once early to start tracking, then call again to read. Returned messages carry timestamps.

**read_network_requests** — Reads HTTP requests (XHR, Fetch, etc.). Same activation pattern as console messages: first call starts tracking. Useful for debugging API calls or confirming that a form submission actually fired.

**navigate** — Go to a URL, or use "back"/"forward" for browser history navigation. The tool's inline Tab Context footer can be stale immediately after navigation, showing the previous URL even though navigation succeeded. If you need to confirm the new URL before the next action, call tabs_context_mcp.

**tabs_context_mcp** — Returns all tabs in the current group. Call this first when starting Chrome work or when recovering from errors to reorient.

**tabs_create_mcp** — Creates a new empty tab in the group.

**tabs_close_mcp** — Closes a tab by ID.

---

## Decision Rule for Screenshots

Before taking a screenshot, ask whether the question is about visual appearance. If not, the answer is in the DOM. Read it directly.

Screenshots are right when the visual layout itself is the question: identifying an unlabeled icon, checking rendering output, confirming something for the user's benefit, or when the user explicitly asks what a page looks like.

Screenshots are wrong for verifying form values (use JS readback or form_input's previous-value report), confirming navigation (check location.href, document.title, or h1), checking for errors (query the error elements), or "looking at the page" before acting (use get_page_text or read_page). A screenshot costs meaningfully more context than a JS readback, and the readback returns structured data rather than pixels.

---

## Verification Pattern

javascript_tool returns the last expression, so combine multiple checks into one round trip by returning an object:

```javascript
({url: location.href, title: document.title, value: el.value, error: document.querySelector('.error')?.innerText})
```

One call writes and verifies, or reads multiple pieces of state at once. This is what makes DOM-first cheaper and more reliable than screenshots rather than just different. Without this pattern, you can use JS but still make five calls where one would do.

---

## Form Filling

form_input handles most cases. When a field resists form_input or sits inside a framework with custom event handlers (React, Vue, Angular), use the native prototype setter pattern to bypass the framework's synthetic event system:

```javascript
const inputSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
const selectSetter = Object.getOwnPropertyDescriptor(window.HTMLSelectElement.prototype, 'value').set;
const checkboxSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'checked').set;

// Text/number inputs:
inputSetter.call(el, value);
el.dispatchEvent(new Event('input', {bubbles: true}));
el.dispatchEvent(new Event('change', {bubbles: true}));
el.dispatchEvent(new Event('blur', {bubbles: true}));

// Select dropdowns:
selectSetter.call(el, value);
el.dispatchEvent(new Event('input', {bubbles: true}));
el.dispatchEvent(new Event('change', {bubbles: true}));

// Checkboxes:
checkboxSetter.call(el, true);
el.dispatchEvent(new Event('click', {bubbles: true}));
el.dispatchEvent(new Event('change', {bubbles: true}));
```

---

## Platform Constraints

As of publication, there is no tool to switch which Chrome tab is active/visible. Plan around this.

Screenshots in background (non-active) tabs can trigger errors for the user. DOM tools are the only reliable option when working in tabs the user is not looking at.

---

## Error Recovery

Chrome tool errors can occur in long sessions. When recovering from an error, use tabs_context_mcp to reorient, then get_page_text or javascript_tool to read the current state. Do not reach for a screenshot to "see where you are" — the DOM is the ground truth, not the pixels.

---

## Render Glitches

Some sites have scroll/render glitches that produce blank-looking screenshots while the DOM is fully populated and saved. Trusting the DOM readback over the visual avoids a class of false-alarm debugging where the AI wastes tool calls re-verifying work that was already done because the visual feedback suggested something had failed.

---

## Documentation

Anthropic's official documentation (capabilities may have changed since this guide was written):

- [Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)
- [Using Claude in Chrome safely](https://support.claude.com/en/articles/12902428-using-claude-in-chrome-safely)
- [Claude in Chrome collection](https://support.claude.com/en/collections/18031491-claude-in-chrome)

---
*Part of [AI Project Architect](https://github.com/vbiroshak/ai-project-architect) — Version 4.6*
