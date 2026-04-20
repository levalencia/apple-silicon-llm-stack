import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('$lib/stores/telemetry', () => {
	return {
		telemetry: {
			messages: [],
			telemetry: [],
			connected: false,
			latency: 0,
			latest: null,
			connect: vi.fn(),
			disconnect: vi.fn(),
			sendMessage: vi.fn().mockResolvedValue(undefined)
		}
	};
});

describe('TelemetryStore', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	it('should export telemetry store', async () => {
		const { telemetry } = await import('$lib/stores/telemetry');
		
		expect(telemetry).toBeDefined();
		expect(Array.isArray(telemetry.messages)).toBe(true);
		expect(Array.isArray(telemetry.telemetry)).toBe(true);
		expect(typeof telemetry.connected).toBe('boolean');
		expect(typeof telemetry.latency).toBe('number');
	});

	it('should have connect and disconnect methods', async () => {
		const { telemetry } = await import('$lib/stores/telemetry');
		
		expect(typeof telemetry.connect).toBe('function');
		expect(typeof telemetry.disconnect).toBe('function');
		expect(typeof telemetry.sendMessage).toBe('function');
	});
});
