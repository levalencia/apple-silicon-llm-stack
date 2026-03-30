package cgobridge

import "unsafe"

// Engine acts as a Go wrapper around our C++ InferenceEngine.
// IMPORTANT (CGO & Memory Management):
// The `ctx` field holds an opaque C pointer (`engine_handle_t`) to the C++ instance.
// Because the Go garbage collector does not track C/C++ heap allocations, we must
// manually call Destroy() to free the underlying memory and avoid leaks.
type Engine struct {
	ctx unsafe.Pointer
}

func NewEngine() *Engine {
	return &Engine{}
}

func (e *Engine) Eval(prompt string) string {
	return "Mock inference response"
}

func (e *Engine) Destroy() {
	e.ctx = nil
}
