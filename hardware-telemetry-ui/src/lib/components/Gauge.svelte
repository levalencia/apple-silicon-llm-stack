<script lang="ts">
	interface Props {
		value: number;
		max: number;
		label: string;
		unit?: string;
	}

	let { value, max, label, unit = '%' }: Props = $props();
	const percentage = $derived(Math.min((value / max) * 100, 100));
	const color = $derived(percentage > 80 ? 'text-red-500' : percentage > 60 ? 'text-yellow-500' : 'text-green-500');
</script>

<div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
	<div class="flex justify-between items-center mb-2">
		<span class="text-gray-400 text-sm">{label}</span>
		<span class="{color} font-mono text-lg">{value.toFixed(1)}{unit}</span>
	</div>
	<div class="h-2 bg-gray-700 rounded-full overflow-hidden">
		<div
			class="h-full transition-all duration-300 {color.replace('text-', 'bg-')}"
			style="width: {percentage}%"
		></div>
	</div>
	<div class="mt-1 text-xs text-gray-500 text-right">0 - {max}{unit}</div>
</div>
