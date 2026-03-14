package model

import "errors"

var (
	ErrInvalidArgument = errors.New("invalid argument")
	ErrOutOfMemory     = errors.New("out of memory")
	ErrModelInvalid    = errors.New("invalid model")
	ErrDeviceNotFound  = errors.New("device not found")
)

type DomainError struct {
	Code    string
	Message string
	Err     error
}

func (e *DomainError) Error() string {
	return e.Message
}

func (e *DomainError) Unwrap() error {
	return e.Err
}

func NewDomainError(code, message string, err error) *DomainError {
	return &DomainError{Code: code, Message: message, Err: err}
}

type Response[T any] struct {
	Success bool   `json:"success"`
	Data    T      `json:"data,omitempty"`
	Error   string `json:"error,omitempty"`
}

type HealthStatus struct {
	Status string `json:"status"`
}

type SSEEvent struct {
	Event string      `json:"event"`
	Data  interface{} `json:"data"`
}
