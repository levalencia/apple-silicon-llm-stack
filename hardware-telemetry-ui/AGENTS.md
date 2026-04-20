# Hardware Telemetry UI Agent Instructions

You are an expert Frontend developer working on the `hardware-telemetry-ui` repository. This is a SvelteKit dashboard built to monitor LLM inference metrics in real-time via Server-Sent Events (SSE) from the Go API Gateway.

## 1. Build, Lint, and Test Commands

When you modify code, always self-verify using these commands from the `hardware-telemetry-ui` directory:

- **Install Dependencies**: `npm install`
- **Run Dev Server**: `npm run dev` (Starts Vite on local port)
- **Production Build**: `npm run build`
- **Type Check & Lint**: `npm run check` (Runs `svelte-check` against `tsconfig.json`)
- **Run All Tests**: `npx vitest run` (Using jsdom environment)
- **Run Single Test**: `npx vitest run src/path/to/test.ts -t "exact test name"`
- **Format Code**: Use Prettier (configured in Svelte workspace)

## 2. Architectural Guidelines

- **Svelte 5 Runes**: (ADR) State management *must* use Svelte 5 Runes (`$state`, `$derived`, `$effect`). Do NOT use the legacy Svelte 4 store syntax (e.g., `writable`, `readable`, `$store`). 
- **Store Pattern**: Centralize business logic and network calls (like SSE connections) inside classes exported from `src/lib/stores/`. See `telemetry.ts` for the correct `$state` class implementation.
- **Server-Sent Events**: Real-time data streams in via SSE from the backend. Handle disconnections and auto-reconnects gracefully within the store classes.
- **Data Visualization**: (ADR) Use raw SVG for highly performant, custom data visualization components (like Gauges) instead of pulling in heavy third-party charting libraries (like Chart.js).

## 3. Code Style & Best Practices

### TypeScript & Types
- **Strict Typing**: The `tsconfig.json` enforces strict mode. You must explicitly type all function arguments, returns, and component props. Never use `any`.
- **Component Props**: Define component props using `$props()` rune (e.g., `let { value, max }: { value: number; max: number } = $props();`).

### Styling & UI
- **Tailwind CSS v4**: All styling must be handled via Tailwind CSS utility classes (`@tailwindcss/vite`).
- **Custom CSS**: Avoid creating `<style>` blocks in Svelte components unless absolutely necessary for complex animations or pseudo-elements that Tailwind struggles with.

### Connectivity
- **API URL**: (ADR-007) Currently hardcoded to `http://localhost:8080`. Point all fetch and EventSource calls here until environment variables are established.

## 4. Agent Operations
- Read `docs/ARCHITECTURE.md` and `docs/DESIGN.md` if modifying data flows or major UI layouts.
- Always check existing components in `src/lib/components/` (like `Gauge.svelte`, `ChatWindow.svelte`) before creating new UI elements to maintain design consistency.
- Remember to use `npm run check` to ensure SvelteKit routing and type contracts remain valid across the app.
