<script lang="ts">
	interface Props {
		connected: boolean;
		latency?: number;
	}

	let { connected, latency = 0 }: Props = $props();
</script>

<div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-800 border border-gray-700">
	<div class="w-2 h-2 rounded-full {connected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}"></div>
	<span class="text-sm text-gray-300">
		{connected ? 'Connected' : 'Disconnected'}
	</span>
	{#if connected && latency > 0}
		<span class="text-xs text-gray-500">• {latency}ms</span>
	{/if}
</div>
