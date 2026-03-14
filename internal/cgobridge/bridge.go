package cgobridge

import "unsafe"

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
