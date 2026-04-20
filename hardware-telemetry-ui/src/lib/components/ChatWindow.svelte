<script lang="ts">
	interface Props {
		messages: Array<{ role: string; content: string }>;
		onSend?: (msg: string) => void;
	}

	let { messages, onSend }: Props = $props();
	let input = $state('');

	function handleSend() {
		if (input.trim() && onSend) {
			onSend(input);
			input = '';
		}
	}

	function handleKey(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSend();
		}
	}
</script>

<div class="flex flex-col h-full bg-gray-900 rounded-lg border border-gray-700">
	<div class="flex-1 overflow-y-auto p-4 space-y-4">
		{#each messages as msg}
			<div class="flex {msg.role === 'user' ? 'justify-end' : 'justify-start'}">
				<div class="max-w-[80%] p-3 rounded-lg {msg.role === 'user' ? 'bg-blue-600' : 'bg-gray-800'}">
					<p class="text-gray-100">{msg.content}</p>
				</div>
			</div>
		{/each}
	</div>
	<div class="border-t border-gray-700 p-4">
		<div class="flex gap-2">
			<input
				type="text"
				bind:value={input}
				onkeydown={handleKey}
				placeholder="Ask about hardware..."
				class="flex-1 bg-gray-800 border border-gray-600 rounded px-4 py-2 text-gray-100 placeholder-gray-400 focus:outline-none focus:border-blue-500"
			/>
			<button
				onclick={handleSend}
				class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white font-medium transition-colors"
			>
				Send
			</button>
		</div>
	</div>
</div>
